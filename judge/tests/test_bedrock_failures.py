"""Offline HTTP recovery and diagnostic publication tests for both Bedrock APIs."""

import json
import math
import unittest
from dataclasses import replace
from datetime import datetime, timezone
from email.utils import format_datetime
from urllib.parse import quote

from judge.bedrock_adapter import BedrockClient, BedrockConfig
from judge.lanes import INITIAL_STAGES
from judge.paired_review import run_paired_review, select_lane_aggregate
from judge.provider_adapter import HttpResponse, JudgeInfraError, TransportError
from judge.tests.helpers import fixture_evidence, review
from judge.tests.test_bedrock_adapter import FakeTransport, StepClock, bedrock_response, sol_response


KEY = "test-bedrock-secret"
MODELS = ("us.anthropic.claude-opus-4-6-v1", "us.openai.gpt-5.6-sol")
NOW = 1700000000.0


def http_error(status=500, *, request_id="aws-failed-1", payload=None, headers=None):
    return HttpResponse(status, {"X-Amzn-RequestId": request_id, **(headers or {})},
                        json.dumps(payload if payload is not None else {
                            "__type": "InternalServerException", "message": "Please try again later.",
                        }).encode())


class BedrockFailureTests(unittest.TestCase):
    def make_client(self, outcomes, *, model=MODELS[0], jitter=0.5, **config):
        transport = FakeTransport(outcomes)
        sleeps = []
        instance = BedrockClient(BedrockConfig(api_key=KEY, model=model, **config),
                                 transport=transport, sleeper=sleeps.append, clock=StepClock(),
                                 wall_clock=lambda: NOW, random_source=lambda: jitter)
        return instance, transport, sleeps

    def test_terminal_http_errors_have_structured_fields_and_latency(self):
        for model in MODELS:
            for status in (301, 400, 401, 403, 404, 413, 422):
                with self.subTest(model=model, status=status):
                    instance, transport, sleeps = self.make_client([http_error(status)], model=model)
                    with self.assertRaises(JudgeInfraError) as caught:
                        instance.review("lane_evaluability", {})
                    error = caught.exception
                    self.assertEqual(error.attempts, 1)
                    self.assertEqual(error.diagnostics, [{
                        "category": "http", "status": status, "stage": "lane_evaluability",
                        "attempt": 1, "latency_ms": 10, "request_id": "aws-failed-1",
                        "error_code": "InternalServerException", "message": "Please try again later.",
                    }])
                    self.assertEqual(len(transport.calls), 1)
                    self.assertEqual(sleeps, [])

    def test_retry_success_preserves_each_error_and_all_attempt_latencies(self):
        for model, response in zip(MODELS, (bedrock_response, sol_response)):
            with self.subTest(model=model):
                failures = [http_error(request_id=f"aws-failed-{i}") for i in (1, 2)]
                instance, transport, sleeps = self.make_client(
                    [*failures, response(review("lane_evaluability"))], model=model)
                result = instance.review("lane_evaluability", {})
                provenance = result.provenance
                self.assertEqual(provenance["attempts"], 3)
                self.assertEqual(provenance["attempt_latencies_ms"], [10, 10, 10])
                self.assertEqual(provenance["latency_ms"], 70)
                self.assertEqual(sleeps, [60.0, 120.0])
                for attempt, detail in enumerate(provenance["retry_diagnostics"], 1):
                    self.assertEqual(detail["request_id"], f"aws-failed-{attempt}")
                    self.assertEqual(detail["attempt"], attempt)
                    self.assertEqual(detail["latency_ms"], 10)
                    self.assertEqual(detail["message"], "Please try again later.")
                    self.assertEqual(detail["error_code"], "InternalServerException")
                self.assertEqual(len(provenance["retry_diagnostics"]), 2)
                # Transient diagnostics are provenance, never model feedback.
                self.assertEqual(len({call["body"] for call in transport.calls}), 1)
                self.assertEqual(len({call["url"] for call in transport.calls}), 1)

    def test_latency_excludes_sleep_per_attempt_but_includes_it_in_total(self):
        now = 0.0
        durations = iter((0.25, 0.5, 1.25))
        def advance(seconds):
            nonlocal now
            now += seconds
        class TimedTransport(FakeTransport):
            def request(self, *args, **kwargs):
                advance(next(durations))
                return super().request(*args, **kwargs)
        transport = TimedTransport([TransportError("private"), http_error(),
                                    bedrock_response(review("lane_cost"))])
        instance = BedrockClient(BedrockConfig(api_key=KEY), transport=transport,
                                 clock=lambda: now, sleeper=advance, random_source=lambda: 0.5)
        result = instance.review("lane_cost", {})
        self.assertEqual(result.provenance["attempt_latencies_ms"], [250, 500, 1250])
        self.assertEqual([d["latency_ms"] for d in result.provenance["retry_diagnostics"]], [250, 500])
        self.assertEqual(result.provenance["latency_ms"], 182000)

    def test_successful_retry_publishes_only_sanitized_failure_fields(self):
        failure = http_error(request_id="aws-" + KEY,
                             headers={"X-Private": "private-header"},
                             payload={"error": {"code": "Internal", "message": "Please retry " + KEY,
                                                "reasoning": "private-error-reasoning"}})
        instance, _, _ = self.make_client([failure, sol_response()], model=MODELS[1])
        provenance = instance.review("lane_evaluability", {}).provenance
        rendered = json.dumps(provenance)
        for excluded in (KEY, "private-header", "private-error-reasoning", "private-reasoning"):
            self.assertNotIn(excluded, rendered)
        detail = provenance["retry_diagnostics"][0]
        self.assertEqual(detail["request_id"], "aws-[REDACTED]")
        self.assertEqual(detail["message"], "Please retry [REDACTED]")

    def test_retryable_http_statuses_stop_at_three_without_final_sleep(self):
        for status in (408, 429, 500, 502, 503, 504, 599):
            with self.subTest(status=status):
                instance, transport, sleeps = self.make_client([http_error(status)] * 3)
                with self.assertRaises(JudgeInfraError) as caught:
                    instance.review("lane_cost", {})
                self.assertEqual(caught.exception.attempts, 3)
                self.assertEqual(len(transport.calls), 3)
                self.assertEqual(sleeps, [60, 120])
                self.assertEqual([d["latency_ms"] for d in caught.exception.diagnostics], [10] * 3)
                self.assertEqual([d["status"] for d in caught.exception.diagnostics], [status] * 3)

    def test_nonretryable_after_transient_failure_keeps_entire_history(self):
        instance, transport, sleeps = self.make_client([
            TransportError("private transport exception " + KEY), http_error(),
            http_error(403, request_id="aws-terminal", payload={"error": {
                "code": "AccessDenied", "message": "Model access denied"}}),
        ], max_attempts=4)
        with self.assertRaises(JudgeInfraError) as caught:
            instance.review("lane_cost", {})
        error = caught.exception
        self.assertEqual(error.attempts, 3)
        self.assertEqual([d["category"] for d in error.diagnostics], ["transport", "http", "http"])
        self.assertEqual([d["latency_ms"] for d in error.diagnostics], [10] * 3)
        self.assertEqual(error.diagnostics[-1]["request_id"], "aws-terminal")
        self.assertEqual(error.diagnostics[-1]["error_code"], "AccessDenied")
        self.assertIn("Model access denied", str(error))
        self.assertEqual(len(transport.calls), 3)
        self.assertEqual(sleeps, [60, 120])
        self.assertNotIn("private transport", str(error) + json.dumps(error.diagnostics))

    def test_transport_exhaustion_never_serializes_exception_text(self):
        instance, _, sleeps = self.make_client([TransportError("private-body " + KEY)] * 3)
        with self.assertRaises(JudgeInfraError) as caught:
            instance.review("lane_cost", {})
        error = caught.exception
        self.assertEqual(error.attempts, 3)
        self.assertEqual(len(error.diagnostics), 3)
        self.assertEqual(sleeps, [60, 120])
        self.assertNotIn(KEY, str(error) + json.dumps(error.diagnostics))
        self.assertNotIn("private-body", str(error) + json.dumps(error.diagnostics))

    def test_redaction_precedes_truncation_for_each_published_field(self):
        for status in (403, 500):
            with self.subTest(status=status):
                instance, _, _ = self.make_client([http_error(status,
                    request_id="r" * 126 + KEY,
                    payload={"error": {"code": "c" * 118 + KEY,
                                       "message": "m" * 298 + KEY}})], max_attempts=1)
                with self.assertRaises(JudgeInfraError) as caught:
                    instance.review("lane_cost", {})
                detail = caught.exception.diagnostics[0]
                for field, length, prefix in (("request_id", 128, "r"), ("error_code", 120, "c"),
                                               ("message", 300, "m")):
                    self.assertEqual(detail[field], prefix * (length - 2) + "[R")
                self.assertNotIn(KEY, str(caught.exception))

    def test_redacts_credentials_and_controls_and_ignores_non_allowlisted_content(self):
        message = (f"Denied {KEY}; Bearer other-credential; api_key=other-key; "
                   'password="other password"; AWS_SECRET_ACCESS_KEY=other-secret; '
                   "\x00\x1b[31m\x7f\x85\u202e\n\tplease retry")
        instance, _, _ = self.make_client([http_error(403,
            request_id=f"req\x1b\u202e{KEY}", headers={"Authorization": "Bearer header-secret",
                                                    "X-Private": "private-header"},
            payload={"error": {"type": f"Internal\x00{KEY}", "message": message,
                               "reasoning": "private-reasoning"},
                     "body": "private-body", "output": "private-output"})])
        with self.assertRaises(JudgeInfraError) as caught:
            instance.review("lane_cost", {})
        detail = caught.exception.diagnostics[0]
        rendered = str(caught.exception) + json.dumps(detail)
        for secret in (KEY, "other-credential", "other-key", "other password", "other-secret",
                       "header-secret", "private-header", "private-reasoning", "private-body", "private-output"):
            self.assertNotIn(secret, rendered)
        for field in ("request_id", "error_code", "message"):
            self.assertTrue(detail[field].isprintable())
        self.assertIn("please retry", detail["message"])
        self.assertIn("[REDACTED]", detail["message"])

    def test_url_encoded_configured_key_is_redacted(self):
        key = "configured/key+with=punctuation"
        instance, _, _ = self.make_client([http_error(403, payload={"message": quote(key, safe="")})])
        instance.config = replace(instance.config, api_key=key)
        with self.assertRaises(JudgeInfraError) as caught:
            instance.review("lane_cost", {})
        self.assertEqual(caught.exception.diagnostics[0]["message"], "[REDACTED]")

    def test_error_envelope_forms_and_header_identifiers(self):
        for payload, expected in (({"__type": "InternalServerException", "Message": "Retry"}, "InternalServerException"),
                                  ({"error": {"type": "server_error", "message": "Retry"}}, "server_error"),
                                  ({"code": 500, "message": "Retry"}, "500")):
            with self.subTest(payload=payload):
                instance, _, _ = self.make_client([http_error(403, payload=payload)])
                with self.assertRaises(JudgeInfraError) as caught:
                    instance.review("lane_cost", {})
                self.assertEqual(caught.exception.diagnostics[0]["error_code"], expected)
                self.assertEqual(caught.exception.diagnostics[0]["message"], "Retry")
        for header in ("X-AMZN-REQUESTID", "X-Amzn-Request-Id", "x-amz-request-id"):
            with self.subTest(header=header):
                response = HttpResponse(503, {header: "aws-id", "X-Amzn-ErrorType": "Unavailable"}, b"not json")
                instance, _, _ = self.make_client([response], max_attempts=1)
                with self.assertRaises(JudgeInfraError) as caught:
                    instance.review("lane_cost", {})
                self.assertEqual(caught.exception.diagnostics[0]["request_id"], "aws-id")
                self.assertEqual(caught.exception.diagnostics[0]["error_code"], "Unavailable")
                self.assertNotIn("message", caught.exception.diagnostics[0])

    def test_non_json_malformed_and_oversized_errors_are_safe(self):
        bodies = [b"<html>private-body</html>", b"\xff", b"null", b"[]", b'"private-body"',
                  b'{"message":"private-body",', b'{"code":true,"message":{}}',
                  b'{"error":["private-body"]}', b'{"message":"private-body","message":"duplicate"}',
                  b'{"message":"private-body","code":NaN}',
                  b'[' * 1500 + b']' * 1500,
                  json.dumps({"message": "private-body" * 6000}).encode()]
        for status in (403, 500):
            for body in bodies:
                with self.subTest(status=status, body_length=len(body)):
                    instance, _, _ = self.make_client([HttpResponse(status, {}, body)], max_attempts=1)
                    with self.assertRaises(JudgeInfraError) as caught:
                        instance.review("lane_cost", {})
                    detail = caught.exception.diagnostics[0]
                    self.assertNotIn("message", detail)
                    self.assertNotIn("error_code", detail)
                    self.assertIsNone(detail["request_id"])
                    self.assertEqual(detail["latency_ms"], 10)
                    self.assertNotIn("private-body", str(caught.exception))

    def test_retry_after_seconds_and_dates_are_bounded_minima(self):
        def http_date(offset):
            return format_datetime(datetime.fromtimestamp(NOW + offset, timezone.utc), usegmt=True)
        cases = {"90": 90, "0.2": 60, "0": 60, "9999999": 120,
                 "-10": 60, "NaN": 60, "Infinity": 60, "-inf": 60, "1e999": 60,
                 "bad date": 60, "": 60, "9" * 200: 60,
                 "Mon, 99 Sep 2026 00:00:00 GMT": 60,
                 "Mon, 28 Sep 99999999 00:00:00 GMT": 60,
                 http_date(90): 90, http_date(600): 120, http_date(-600): 60}
        for value, expected in cases.items():
            with self.subTest(value=value):
                instance, _, sleeps = self.make_client([
                    http_error(headers={"rEtRy-AfTeR": value}), bedrock_response(review("lane_cost"))])
                instance.review("lane_cost", {})
                self.assertEqual(sleeps, [expected])
                self.assertTrue(all(math.isfinite(delay) and 0 <= delay <= 120 for delay in sleeps))

    def test_jitter_cannot_exceed_cap_and_large_attempt_does_not_overflow(self):
        for jitter, expected in ((0.0, [45, 90]), (1.0, [75, 120])):
            instance, _, sleeps = self.make_client([http_error()] * 3, jitter=jitter)
            with self.assertRaises(JudgeInfraError):
                instance.review("lane_cost", {})
            self.assertEqual(sleeps, expected)
            self.assertLessEqual(instance._retry_delay(10000, transient=True), 120)

    def test_invalid_retry_config_rejected_before_request(self):
        for field in ("base_retry_seconds", "max_retry_seconds", "transient_base_retry_seconds",
                      "transient_max_retry_seconds"):
            for value in (-1, 0, math.nan, math.inf):
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    BedrockConfig(api_key=KEY, **{field: value})
        for config in ({"transient_base_retry_seconds": 121}, {"base_retry_seconds": 9},
                       {"max_attempts": 0}, {"max_attempts": True}, {"max_attempts": 1.5}):
            with self.subTest(config=config), self.assertRaises(ValueError):
                BedrockConfig(api_key=KEY, **config)

    def test_explicit_one_call_probe_never_retries_any_failure(self):
        for outcome in (http_error(), http_error(429), TransportError("private-body"),
                        sol_response(status="incomplete")):
            instance, transport, sleeps = self.make_client([outcome], model=MODELS[1], max_attempts=1)
            with self.assertRaises(JudgeInfraError) as caught:
                instance.review("lane_cost", {})
            self.assertEqual(caught.exception.attempts, 1)
            self.assertEqual(len(transport.calls), 1)
            self.assertEqual(sleeps, [])

    def test_validation_budget_stays_three_with_short_delays_and_latency(self):
        for outcomes, expected in (([sol_response(status="incomplete")] * 3, [0.5, 1]),
                                   ([sol_response(status="incomplete"), http_error(),
                                     sol_response(status="incomplete")], [0.5, 120])):
            instance, transport, sleeps = self.make_client(outcomes, model=MODELS[1])
            with self.assertRaises(JudgeInfraError) as caught:
                instance.review("lane_cost", {})
            self.assertEqual(caught.exception.attempts, 3)
            self.assertEqual(len(transport.calls), 3)
            self.assertEqual(sleeps, expected)
            self.assertEqual([d["latency_ms"] for d in caught.exception.diagnostics], [10] * 3)
            self.assertIn("previous response could not be processed", transport.calls[1]["body"].decode())

    def test_request_id_sanitization_applies_to_validation_and_success_provenance(self):
        for model, response in zip(MODELS, (bedrock_response, sol_response)):
            for valid in (True, False):
                with self.subTest(model=model, valid=valid):
                    original = response(review("lane_cost"))
                    wire = HttpResponse(200, {"x-amzn-requestid": "aws\x1b" + KEY}, original.body if valid else b"{}")
                    instance, _, _ = self.make_client([wire], model=model, max_attempts=1)
                    if valid:
                        provenance = instance.review("lane_cost", {}).provenance
                        field = "aws_request_id" if model == MODELS[1] else "response_id"
                        self.assertEqual(provenance[field], "aws [REDACTED]")
                    else:
                        with self.assertRaises(JudgeInfraError) as caught:
                            instance.review("lane_cost", {})
                        self.assertEqual(caught.exception.diagnostics[0]["request_id"], "aws [REDACTED]")

    def test_paired_dossier_preserves_terminal_and_successful_retry_diagnostics(self):
        for model, response in zip(MODELS, (bedrock_response, sol_response)):
            for terminal in (False, True):
                with self.subTest(model=model, terminal=terminal):
                    outcomes = [http_error(request_id=f"aws-failed-{i}") for i in (1, 2, 3) if terminal or i == 1]
                    outcomes += [response(review(stage)) for stage in INITIAL_STAGES
                                 if not terminal or stage != "lane_evaluability"]
                    instance, _, _ = self.make_client(outcomes, model=model)
                    dossier = run_paired_review(fixture_evidence(), instance)
                    if terminal:
                        failure = dossier["failure_diagnostics"]["lane_evaluability"]
                        self.assertEqual(failure["attempts"], 3)
                        details = failure["errors"]
                        self.assertEqual(len(details), 3)
                        for lane in ("exploratory", "rigorous"):
                            selected = select_lane_aggregate(dossier, lane)
                            self.assertEqual(selected["status"], "infra_failed")
                            self.assertFalse(selected["eligible"])
                        self.assertIn("Please try again later.", dossier["infrastructure_failures"]["lane_evaluability"])
                    else:
                        details = dossier["provenance"]["lane_evaluability"]["retry_diagnostics"]
                        self.assertEqual(len(details), 1)
                        self.assertEqual(dossier["lanes"]["rigorous"]["status"], "ai_rigor_qualified")
                    for i, detail in enumerate(details, 1):
                        self.assertEqual(detail["request_id"], f"aws-failed-{i}")
                        self.assertEqual(detail["error_code"], "InternalServerException")
                        self.assertEqual(detail["message"], "Please try again later.")
                        self.assertEqual(detail["latency_ms"], 10)
                    self.assertNotIn(KEY, json.dumps(dossier))


if __name__ == "__main__":
    unittest.main()
