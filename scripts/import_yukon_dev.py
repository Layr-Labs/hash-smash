#!/usr/bin/env python3
"""Plan or submit one real HashSmash leaf import to Yukon dev. Never opens it."""

import argparse
import json
import os
from pathlib import Path
import re
import sys
import time
from urllib import error, parse, request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from verifier.frontier_tracks import get_frontier_track
from verifier.intake import validate_candidate

API_URL = "https://yukon-api-dev.fly.dev"
SOURCE_URL = "https://github.com/Layr-Labs/hash-smash"


class ImportFailure(Exception):
    pass


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Do not forward the importer credential to a redirected host.
        return None


def import_request(lane, branch="main", name=None):
    if lane not in {"exploratory", "rigorous"}:
        raise ImportFailure("select a defined HashSmash lane")
    if not branch or len(branch) > 255 or any(ord(char) < 32 for char in branch):
        raise ImportFailure("invalid source branch")
    payload = {"sourceUrl": SOURCE_URL, "sourceBranch": branch,
               "rootDir": f"lanes/{lane}"}
    if name is not None:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*/[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ImportFailure("name must be the confirmed setter/challenge slug")
        payload["name"] = name
    return payload


def draft_tracks(lane):
    manifest = json.loads((ROOT / "lanes" / lane / "benchmark.json").read_bytes())
    drafts = []
    for entry in manifest["tracks"]:
        track = get_frontier_track(f"{entry['name']}-{lane}")
        intake = validate_candidate(track.candidate, track=track)
        if intake["submission_state"] != "ready":
            drafts.append(track.id)
    return drafts


def importer_token(filename=None):
    if filename:
        path = Path(filename).expanduser().resolve(strict=True)
        if path.is_relative_to(ROOT) or path.name == ".env":
            raise ImportFailure("keep the importer key in a separate file outside the repository")
        if path.stat().st_mode & 0o077:
            raise ImportFailure("importer key file must be private to its owner (chmod 600)")
        if path.stat().st_size > 8192:
            raise ImportFailure("importer key file is too large")
        token = path.read_text().strip()
    else:
        token = (os.environ.get("YUKON_API_KEY") or os.environ.get("YUKON_API_TOKEN") or "").strip()
    if not token or any(char.isspace() for char in token):
        raise ImportFailure("provide an allowlisted dev importer key through --api-key-file or YUKON_API_KEY")
    return token


class DevClient:
    def __init__(self, token):
        self.token = token
        self.opener = request.build_opener(NoRedirect())

    def call(self, path, payload=None):
        if not path.startswith("/api/") or "?" in path or "#" in path:
            raise ImportFailure("invalid Yukon API path")
        data = None if payload is None else json.dumps(payload).encode()
        req = request.Request(API_URL + path, data=data, headers={
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json", "Accept": "application/json",
        })
        try:
            with self.opener.open(req, timeout=60) as response:
                return json.load(response)
        except error.HTTPError as failure:
            message = f"Yukon dev returned HTTP {failure.code}."
            if failure.code in (401, 403):
                message += " Check the dev key and its account email's importer allowlist access."
            elif failure.code == 409:
                message += " Inspect the existing dev import before retrying."
            if payload is not None and failure.code >= 500:
                message += " The import outcome may be unknown; inspect dev before retrying."
            raise ImportFailure(message) from None
        except (error.URLError, TimeoutError, OSError, ValueError):
            message = "Could not read a valid response from Yukon dev."
            if payload is not None:
                message += " The import outcome is unknown; inspect dev before retrying. No retry was sent."
            raise ImportFailure(message) from None


def queued_tracks(response):
    tracks = response.get("tracks")
    if not isinstance(tracks, list) or not tracks:
        raise ImportFailure("unexpected import response; inspect dev before retrying")
    for track in tracks:
        if not isinstance(track, dict) or not isinstance(track.get("id"), str):
            raise ImportFailure("invalid track in import response; inspect dev before retrying")
    return tracks


def wait_for_baselines(client, tracks, timeout):
    deadline = time.monotonic() + timeout
    pending = {track["id"]: track for track in tracks}
    statuses = {}
    failed = False
    while pending:
        for identifier in list(pending):
            result = client.call("/api/benchmarks/" + parse.quote(identifier, safe=""))["benchmark"]
            status = result["status"]
            if statuses.get(identifier) != status:
                print(json.dumps({"id": identifier, "name": result["name"], "status": status}), flush=True)
                statuses[identifier] = status
            if status in {"ready", "failed", "open", "closed"}:
                failed |= status != "ready"
                del pending[identifier]
        if not pending:
            return 2 if failed else 0
        if time.monotonic() >= deadline:
            raise ImportFailure("Timed out waiting. Existing jobs continue; inspect dev instead of re-importing.")
        time.sleep(min(15, max(0, deadline - time.monotonic())))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lane", required=True, choices=("exploratory", "rigorous"))
    parser.add_argument("--source-branch", default="main")
    parser.add_argument("--name", help="confirmed setter/challenge slug; otherwise Yukon chooses it")
    parser.add_argument("--api-key-file", help="private key file outside the repository; never printed")
    parser.add_argument("--submit", action="store_true", help="create the dev import; default only prints a plan")
    parser.add_argument("--wait", action="store_true", help="wait for baseline validation after submitting")
    parser.add_argument("--timeout", type=int, default=4200, help="baseline wait seconds (default 4200)")
    args = parser.parse_args(argv)
    if args.timeout <= 0 or (args.wait and not args.submit):
        parser.error("timeout must be positive; --wait requires --submit")
    try:
        payload = import_request(args.lane, args.source_branch, args.name)
        drafts = draft_tracks(args.lane)
        manifest = json.loads((ROOT / payload["rootDir"] / "benchmark.json").read_bytes())
        print(json.dumps({"api": API_URL, "request": payload,
                          "baseline_workflows": len(manifest["tracks"]),
                          "local_drafts": drafts, "opens_challenge": False}, indent=2), flush=True)
        if not args.submit:
            return 0
        if drafts:
            raise ImportFailure("Complete and qualify the real candidates before importing; local drafts remain.")
        client = DevClient(importer_token(args.api_key_file))
        tracks = queued_tracks(client.call("/api/benchmarks", payload))
        for track in tracks:
            print(json.dumps({"id": track["id"], "name": track.get("name"),
                              "jobs_url": API_URL + "/api/benchmarks/" + parse.quote(track["id"], safe="") + "/jobs"}), flush=True)
        return wait_for_baselines(client, tracks, args.timeout) if args.wait else 0
    except (ImportFailure, OSError, ValueError) as failure:
        # No request headers, token, or provider environment enters the output.
        print(f"Dev import stopped: {failure}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
