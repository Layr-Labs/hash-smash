"""Bounded organizer evaluators and isolated submitted Python evidence.

No candidate paths are opened here. Intake supplies immutable, hash-checked byte
snapshots. Only those bytes enter an ephemeral, secret-free Docker container.
An executed report is evidence at its stated scope, never an attack-cost proof.
"""

from __future__ import annotations

import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import selectors
import shutil
import subprocess
import tempfile
import time
import tokenize
from dataclasses import asdict, dataclass
from typing import Any, Callable, Mapping
import uuid


DEFAULT_DOCKER_IMAGE = (
    "python:3.12.12-slim-bookworm@sha256:"
    "2986c55feb36e6cae00fa1fefb454283e4b33f35e75ff8bdd123b134130be301"
)
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}\Z")
_PROGRAM = re.compile(r"experiments/[A-Za-z0-9][A-Za-z0-9_-]{0,63}\.py\Z")
_HASH = re.compile(r"[0-9a-f]{64}\Z")
_HEX = re.compile(r"(?:[0-9a-f]{2})+\Z")
_IMAGE = re.compile(r"(?:docker\.io/library/)?python:[A-Za-z0-9._-]+@sha256:[0-9a-f]{64}\Z")
KINDS = {"addition-xor-exact-v1", "addition-xor-sampled-v1", "python-message-pairs-v1"}


class ExperimentError(ValueError):
    """An experiment failed a deterministic validation or execution gate."""


class ExperimentSetupError(ExperimentError):
    """The organizer's isolated executor is unavailable or misconfigured."""


@dataclass(frozen=True)
class ExperimentLimits:
    """Organizer budgets; a participant manifest cannot increase these values."""

    trials: int = 256
    exact_word_bits: int = 8
    max_source_bytes: int = 64 * 1024
    max_message_bytes: int = 4096
    max_output_bytes: int = 2 * 1024 * 1024
    timeout_seconds: float = 20.0
    memory_mb: int = 128
    pids: int = 32
    confidence_alpha: float = 0.01

    def __post_init__(self) -> None:
        for name, lower, upper in (
            ("trials", 1, 4096), ("exact_word_bits", 1, 10),
            ("max_source_bytes", 1, 262144), ("max_message_bytes", 1, 65536),
            ("max_output_bytes", 128, 16 * 1024 * 1024),
            ("memory_mb", 32, 512), ("pids", 8, 64),
        ):
            value = getattr(self, name)
            if type(value) is not int or not lower <= value <= upper:
                raise ExperimentError(f"organizer limit {name} outside permitted range")
        if type(self.timeout_seconds) not in (int, float) or not 0 < self.timeout_seconds <= 120:
            raise ExperimentError("organizer timeout must be between zero and 120 seconds")
        if type(self.confidence_alpha) not in (int, float) or not 0 < self.confidence_alpha < 1:
            raise ExperimentError("organizer confidence_alpha must be between zero and one")


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("utf-8")


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _keys(value: Any, required: set[str], optional: set[str] = frozenset()) -> None:
    if type(value) is not dict or not required <= set(value) or set(value) - required - optional:
        raise ExperimentError("experiment object contains missing or unexpected fields")


def _text(value: Any, name: str, limit: int = 2000) -> None:
    if type(value) is not str or not value.strip() or len(value) > limit or "\x00" in value:
        raise ExperimentError(f"{name}: nonempty bounded text required")


def validate_manifest(manifest: Any) -> dict[str, Any]:
    """Validate a closed manifest and return a detached JSON-normalized copy."""
    _keys(manifest, {"schema_version", "experiments"})
    if type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1:
        raise ExperimentError("experiment manifest schema_version must be 1")
    entries = manifest["experiments"]
    if type(entries) is not list or not 1 <= len(entries) <= 16:
        raise ExperimentError("experiment manifest requires 1 to 16 entries")
    ids: set[str] = set()
    for entry in entries:
        if type(entry) is not dict or type(entry.get("kind")) is not str or entry["kind"] not in KINDS:
            raise ExperimentError("unsupported experiment kind")
        common = {"id", "kind", "scope", "hypothesis"}
        if entry["kind"] == "python-message-pairs-v1":
            _keys(entry, common | {"program", "event"})
            if type(entry["program"]) is not str or not _PROGRAM.fullmatch(entry["program"]):
                raise ExperimentError("program must be a direct experiments/<basename>.py file")
            event = entry["event"]
            if type(event) is not dict:
                raise ExperimentError("Python experiment needs an explicit checked event")
            if event.get("kind") == "full-collision":
                _keys(event, {"kind"})
            elif event.get("kind") == "digest-xor-mask":
                _keys(event, {"kind", "mask_hex", "expected_hex"})
                mask, expected = event["mask_hex"], event["expected_hex"]
                if any(type(x) is not str or not _HEX.fullmatch(x) for x in (mask, expected)):
                    raise ExperimentError("event mask/expected must be lowercase even-length hex")
                if len(mask) != len(expected) or not 2 <= len(mask) <= 256:
                    raise ExperimentError("event mask and expected must have equal bounded lengths")
                if int(mask, 16) == 0 or int(expected, 16) & ~int(mask, 16):
                    raise ExperimentError("event needs a nonzero mask and expected bits inside mask")
            else:
                raise ExperimentError("unsupported checked event")
        else:
            _keys(entry, common | {"word_bits", "input_xor_a", "input_xor_b", "output_xor"})
            bits = entry["word_bits"]
            if type(bits) is not int or not 1 <= bits <= 32:
                raise ExperimentError("word_bits must be an integer in 1..32")
            for field in ("input_xor_a", "input_xor_b", "output_xor"):
                if type(entry[field]) is not int or not 0 <= entry[field] < 1 << bits:
                    raise ExperimentError(f"{field}: value does not fit word_bits")
        identifier = entry["id"]
        if type(identifier) is not str or not _ID.fullmatch(identifier) or identifier in ids:
            raise ExperimentError("experiment ids must be valid and unique")
        ids.add(identifier)
        _text(entry["scope"], "scope")
        _text(entry["hypothesis"], "hypothesis")
    return json.loads(_canonical(manifest))


def declared_files(manifest: Any) -> set[str]:
    return {entry["program"] for entry in validate_manifest(manifest)["experiments"] if "program" in entry}


def _snapshots(manifest: dict[str, Any], file_bytes: Mapping[str, bytes], limits: ExperimentLimits) -> dict[str, bytes]:
    if set(file_bytes) != declared_files(manifest):
        raise ExperimentError("experiment source mapping must contain exactly the declared programs")
    result = {}
    for path, data in file_bytes.items():
        if type(data) is not bytes or len(data) > limits.max_source_bytes:
            raise ExperimentError("experiment source must be a bounded immutable byte snapshot")
        try:
            source = data.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ExperimentError("experiment source must be UTF-8") from error
        if not source.strip() or "\x00" in source:
            raise ExperimentError("experiment source must be nonempty and NUL-free")
        try:
            encoding, _ = tokenize.detect_encoding(io.BytesIO(data).readline)
        except (SyntaxError, LookupError) as error:
            raise ExperimentError("experiment source must use Python UTF-8 encoding") from error
        if encoding not in {"utf-8", "utf-8-sig"}:
            raise ExperimentError("experiment source encoding must be UTF-8 so executed text matches judge source")
        result[path] = data
    return result


def _trial_seed(seed_material: bytes, identifier: str, trial: int) -> str:
    return _sha(seed_material + _canonical([identifier, trial]))


def _addition(entry: dict[str, Any], limits: ExperimentLimits, seed_material: bytes) -> dict[str, Any]:
    bits = entry["word_bits"]
    modulus, mask = 1 << bits, (1 << bits) - 1
    exact = entry["kind"] == "addition-xor-exact-v1"
    if exact and bits > limits.exact_word_bits:
        raise ExperimentError("exact addition exceeds organizer exhaustive word-size budget")
    trials = modulus * modulus if exact else limits.trials
    successes = 0
    for index in range(trials):
        if exact:
            a, b = divmod(index, modulus)
        else:
            random_bytes = hashlib.shake_256(bytes.fromhex(_trial_seed(seed_material, entry["id"], index))).digest(8)
            a, b = int.from_bytes(random_bytes[:4], "big") & mask, int.from_bytes(random_bytes[4:], "big") & mask
        observed = ((a+b) & mask) ^ (((a ^ entry["input_xor_a"])+(b ^ entry["input_xor_b"])) & mask)
        successes += observed == entry["output_xor"]
    result: dict[str, Any] = {
        "trials": trials, "successes": successes,
        "event": "((a+b) mod 2^w) XOR (((a XOR da)+(b XOR db)) mod 2^w) == dc",
        "distribution": f"uniform ordered pairs in [0, 2^{bits})^2",
        "predicate_trust": "organizer_recomputed", "cost_trust": "no_attack_cost_inference",
        "scope_limit": "One modular addition at the declared width; no full-trail or round-independence conclusion.",
    }
    if exact:
        result["evidence_class"] = "exact_finite_count"
        result["probability"] = {"numerator": successes, "denominator": trials}
    else:
        epsilon = math.sqrt(math.log(2 / limits.confidence_alpha) / (2 * trials))
        result["evidence_class"] = "deterministic_sample"
        result["frequency"] = successes / trials
        result["interval"] = {
            "method": "two-sided-hoeffding", "alpha": limits.confidence_alpha,
            "lower": max(0.0, successes / trials - epsilon),
            "upper": min(1.0, successes / trials + epsilon),
            "assumption": "Interval coverage assumes independent uniform samples. Fixed SHAKE-derived seeds provide reproducibility, not an unconditional randomness theorem. No adaptive stopping; no multiple-comparison adjustment.",
        }
    return result


def _docker_command(binary: str, image: str, directory: Path, name: str, limits: ExperimentLimits) -> list[str]:
    """Build the complete fixed isolation policy; no candidate argument is inserted."""
    return [
        binary, "run", "--rm", "--pull=never", "--platform=linux/amd64", "--name", name,
        "--network=none", "--read-only", "--cap-drop=ALL", "--log-driver=none",
        "--security-opt=no-new-privileges", "--user=65534:65534",
        "--cpus=1", f"--memory={limits.memory_mb}m", f"--memory-swap={limits.memory_mb}m",
        f"--pids-limit={limits.pids}", "--ulimit=nofile=64:64", "--ulimit=core=0:0",
        "--ipc=none", "--tmpfs=/tmp:rw,noexec,nosuid,nodev,size=16m,mode=1777",
        "--mount", f"type=bind,src={directory},dst=/input,readonly",
        "--workdir=/tmp", "--env=PYTHONHASHSEED=0", "--env=PYTHONDONTWRITEBYTECODE=1",
        "--env=PYTHONUNBUFFERED=1", "--env=LANG=C.UTF-8", "--env=LC_ALL=C.UTF-8",
        "--entrypoint=python", "-i", image, "-B", "-s", "-P", "/input/program.py",
    ]


def _run_docker(source: bytes, request: dict[str, Any], limits: ExperimentLimits, image: str) -> bytes:
    if type(image) is not str or not _IMAGE.fullmatch(image):
        raise ExperimentSetupError("Python executor requires an official python image pinned by sha256 digest")
    binary = shutil.which("docker")
    if binary is None:
        raise ExperimentSetupError("Docker is unavailable; participant Python has no host execution fallback")
    name = "hashsmash-experiment-" + uuid.uuid4().hex
    # Docker CLI has no inherited cloud/provider secrets. Config directory is a
    # new empty directory: no registry credentials or user Docker configuration.
    environment = {"PATH": os.path.dirname(binary) + ":/usr/bin:/bin"}
    # Preserve only an explicit organizer Docker socket location, never credentials.
    if os.environ.get("DOCKER_HOST", "").startswith("unix://"):
        environment["DOCKER_HOST"] = os.environ["DOCKER_HOST"]
    elif Path("/var/run/docker.sock").exists():
        environment["DOCKER_HOST"] = "unix:///var/run/docker.sock"
    elif Path.home().joinpath(".docker/run/docker.sock").exists():
        environment["DOCKER_HOST"] = "unix://" + str(Path.home().joinpath(".docker/run/docker.sock"))
    try:
        with tempfile.TemporaryDirectory(prefix="hashsmash-experiment-") as temporary:
            root = Path(temporary)
            inputs = root / "input"
            inputs.mkdir(mode=0o755)
            (inputs / "program.py").write_bytes(source)
            (inputs / "program.py").chmod(0o444)
            config = root / "docker-config"
            config.mkdir()
            environment["DOCKER_CONFIG"] = str(config)
            try:
                available = subprocess.run([binary, "image", "inspect", image],
                    stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    env=environment, timeout=10, check=False)
            except subprocess.TimeoutExpired as error:
                raise ExperimentSetupError("Docker image/daemon preflight timed out") from error
            if available.returncode != 0:
                raise ExperimentSetupError("Docker daemon, pinned image or socket permission is unavailable")
            request_path = root / "request.json"
            request_path.write_bytes(_canonical(request) + b"\n")
            output = bytearray()
            output_size = 0
            with request_path.open("rb") as stdin:
                process = subprocess.Popen(_docker_command(binary, image, inputs, name, limits), stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=environment)
                deadline = time.monotonic() + limits.timeout_seconds
                violation = None
                with selectors.DefaultSelector() as selector:
                    selector.register(process.stdout, selectors.EVENT_READ, "stdout")
                    selector.register(process.stderr, selectors.EVENT_READ, "stderr")
                    while selector.get_map():
                        if time.monotonic() > deadline:
                            violation = "Python experiment exceeded organizer timeout"
                            break
                        for key, _ in selector.select(timeout=0.05):
                            chunk = os.read(key.fd, 65536)
                            if not chunk:
                                selector.unregister(key.fileobj)
                                continue
                            output_size += len(chunk)
                            if output_size > limits.max_output_bytes:
                                violation = "Python experiment exceeded organizer output budget"
                                break
                            if key.data == "stdout":
                                output.extend(chunk)
                        if violation:
                            break
                if violation:
                    process.kill()
                    process.wait(timeout=5)
                    process.stdout.close()
                    process.stderr.close()
                    raise ExperimentError(violation)
                process.stdout.close()
                process.stderr.close()
                try:
                    process.wait(timeout=max(0.01, deadline-time.monotonic()))
                except subprocess.TimeoutExpired as error:
                    process.kill()
                    process.wait(timeout=5)
                    raise ExperimentError("Python experiment exceeded organizer timeout") from error
            if process.returncode != 0:
                if process.returncode == 125:
                    raise ExperimentSetupError("Docker could not start the pinned isolated executor; check daemon, image digest and permissions")
                raise ExperimentError(f"Python experiment failed with exit status {process.returncode}; participant stderr is not a trusted report")
            return bytes(output)
    except OSError as error:
        raise ExperimentSetupError("could not start isolated Docker executor") from error
    finally:
        # Fixed generated name; never remove any user container or broader object.
        try:
            subprocess.run([binary, "rm", "-f", name], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=environment, timeout=10, check=False)
        except (OSError, subprocess.TimeoutExpired):
            pass


def _strict_json(data: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        value = {}
        for key, item in items:
            if key in value:
                raise ExperimentError("Python output has duplicate JSON keys")
            value[key] = item
        return value
    def bad_number(_: str) -> None:
        raise ExperimentError("Python output contains nonfinite JSON number")
    try:
        return json.loads(data, object_pairs_hook=pairs, parse_constant=bad_number)
    except (ValueError, UnicodeDecodeError, RecursionError) as error:
        raise ExperimentError("Python output must be one bounded strict JSON document") from error


def _python_result(entry: dict[str, Any], source: bytes, limits: ExperimentLimits, seed_material: bytes, target_profile: str, digest_fn: Callable[[bytes], bytes], docker_image: str) -> dict[str, Any]:
    request = {
        "schema_version": 1, "experiment_id": entry["id"], "target_profile": target_profile,
        "event": entry["event"], "max_message_bytes": limits.max_message_bytes,
        "trials": [{"trial": index, "seed": _trial_seed(seed_material, entry["id"], index)} for index in range(limits.trials)],
    }
    output = _run_docker(source, request, limits, docker_image)
    result = _strict_json(output)
    _keys(result, {"schema_version", "trials"})
    if type(result["schema_version"]) is not int or result["schema_version"] != 1 or type(result["trials"]) is not list or len(result["trials"]) != limits.trials:
        raise ExperimentError("Python output must report exactly every organizer trial")
    sample_digest = digest_fn(b"")
    if type(sample_digest) is not bytes or not sample_digest:
        raise ExperimentSetupError("selected target digest callback must return nonempty bytes")
    event = entry["event"]
    if event["kind"] == "digest-xor-mask" and len(event["mask_hex"]) != 2 * len(sample_digest):
        raise ExperimentError("event mask length does not match selected target digest")
    rows, successes = [], 0
    pairs_seen: set[str] = set()
    for index, row in enumerate(result["trials"]):
        _keys(row, {"trial", "message_a_hex", "message_b_hex"}, {"observations"})
        if type(row["trial"]) is not int or row["trial"] != index:
            raise ExperimentError("Python trials must appear exactly once in organizer order")
        observations = row.get("observations", {})
        if type(observations) is not dict or len(observations) > 16:
            raise ExperimentError("observations must be a bounded numeric object")
        for key, value in observations.items():
            if type(key) is not str or not _ID.fullmatch(key) or type(value) not in (int, float, bool) or (type(value) in (int, float) and not -1e100 <= value <= 1e100):
                raise ExperimentError("observations must have simple ids and finite bounded numeric values")
        values = row["message_a_hex"], row["message_b_hex"]
        if values == (None, None):
            checked = {"trial": index, "success": False, "reason": "no_pair_returned"}
        else:
            if any(type(value) is not str or len(value) > 2 * limits.max_message_bytes or (value and not _HEX.fullmatch(value)) for value in values):
                raise ExperimentError("Python messages require bounded lowercase hex or two nulls")
            message_a, message_b = (bytes.fromhex(value) for value in values)
            digest_a, digest_b = digest_fn(message_a), digest_fn(message_b)
            if any(type(value) is not bytes or len(value) != len(sample_digest) for value in (digest_a, digest_b)):
                raise ExperimentSetupError("inconsistent selected target digest callback")
            collision = message_a != message_b and digest_a == digest_b
            if event["kind"] == "full-collision":
                success = collision
            else:
                success = message_a != message_b and ((int.from_bytes(digest_a, "big") ^ int.from_bytes(digest_b, "big")) & int(event["mask_hex"], 16)) == int(event["expected_hex"], 16)
            pair_id = _sha(_canonical(sorted(values)))
            checked = {
                "trial": index, "success": success, "full_collision": collision,
                "message_a_hex": values[0], "message_b_hex": values[1],
                "digest_a_hex": digest_a.hex(), "digest_b_hex": digest_b.hex(),
                "pair_sha256": pair_id, "repeated_pair": pair_id in pairs_seen,
            }
            pairs_seen.add(pair_id)
            successes += success
        if observations:
            checked["untrusted_participant_observations"] = observations
        rows.append(checked)
    replay = _run_docker(source, request, limits, docker_image)
    if replay != output:
        raise ExperimentError("Python experiment is not reproducible for the identical organizer request")
    return {
        "evidence_class": "executed_witness_trials", "trials": limits.trials, "successes": successes,
        "event": event, "predicate_trust": "organizer_recomputed", "cost_trust": "no_attack_cost_inference",
        "probability_inference": "none: participant program may couple trials, ignore seeds or replay pairs; frequency is not an iid success-probability estimate",
        "scope_limit": "Only the selected-target output event on returned pairs was checked. Internal predicates, algorithmic work, extrapolation and expected cost remain unverified.",
        "sandbox_image": docker_image, "sandbox_platform": "linux/amd64", "request_sha256": _sha(_canonical(request)),
        "stdout_sha256": _sha(output), "checked_trials": rows,
        "reproducibility": {"identical_request_runs": 2, "stdout_byte_identical": True,
                            "scope": "Two fresh isolated executions only; not a proof for all future runs or seeds."},
        "organizer_digest_evaluations": 1 + 2 * sum("message_a_hex" in row for row in rows),
    }


def run_experiments(manifest: Any, file_bytes: Mapping[str, bytes], *, target_profile: str, target_config_sha256: str, digest_fn: Callable[[bytes], bytes] | None = None, limits: ExperimentLimits = ExperimentLimits(), seed: str = "hashsmash-public-seed-v1", holdout_nonce: str | None = None, docker_image: str | None = None) -> dict[str, Any]:
    """Evaluate an immutable evidence snapshot using organizer-owned settings.

    ``holdout_nonce`` must be selected after candidate commitment for a holdout
    claim. Supplying it here does not itself establish that temporal commitment.
    No filesystem path, command, target callback or execution budget comes from
    the candidate. Exceptions mean no completed evidence report exists.
    """
    normalized = validate_manifest(manifest)
    sources = _snapshots(normalized, file_bytes, limits)
    _text(target_profile, "target_profile", 256)
    if type(target_config_sha256) is not str or not _HASH.fullmatch(target_config_sha256):
        raise ExperimentError("target_config_sha256 must be a trusted lowercase SHA-256")
    _text(seed, "organizer seed", 256)
    if holdout_nonce is not None:
        _text(holdout_nonce, "organizer holdout nonce", 256)
    seed_material = _canonical({"domain": "hashsmash-experiments-v1", "seed": seed, "holdout_nonce": holdout_nonce, "target_config_sha256": target_config_sha256})
    results = []
    for entry in normalized["experiments"]:
        if entry["kind"] == "python-message-pairs-v1":
            if digest_fn is None:
                raise ExperimentSetupError("Python message-pair experiments require the trusted selected-target digest callback")
            measured = _python_result(entry, sources[entry["program"]], limits, seed_material, target_profile, digest_fn, docker_image or DEFAULT_DOCKER_IMAGE)
        else:
            measured = _addition(entry, limits, seed_material)
        results.append({"id": entry["id"], "kind": entry["kind"], "status": "completed", "scope": entry["scope"], "hypothesis": entry["hypothesis"], **measured})
    report = {
        "schema_version": 1, "status": "completed", "executor": "hashsmash-experiments-v1",
        "target_profile": target_profile, "target_config_sha256": target_config_sha256,
        "manifest_sha256": _sha(_canonical(normalized)), "manifest": normalized,
        "organizer_limits": asdict(limits), "seed": seed, "holdout_nonce": holdout_nonce,
        "seed_protocol": "sha256(canonical organizer seed material || canonical [experiment id, trial index]); fixed after commitment for genuine holdout testing",
        "selection_bias_warning": "Public-seed experiments may have been selected for favorable outcomes. A supplied holdout nonce alone does not prove prior commitment. No correction for participant searches or multiple comparisons.",
        "sources": [{"path": path, "sha256": _sha(data), "size_bytes": len(data), "untrusted_source_text": data.decode("utf-8")} for path, data in sorted(sources.items())],
        "experiments": results,
        "interpretation": "Evidence only at each declared measured scope; no automatic claim qualification, full-scale probability, expected work or score follows from this report.",
    }
    report["report_sha256"] = _sha(_canonical(report))
    return report


def verify_report_integrity(report: Any) -> dict[str, Any]:
    """Detect accidental/stale changes, not authenticate hostile claimed reports.

    Reports must originate from a trusted organizer artifact/job. A candidate can
    recompute a hash and is never allowed to supply this report as authoritative.
    """
    required = {"schema_version", "status", "executor", "target_profile", "target_config_sha256", "manifest_sha256", "manifest", "organizer_limits", "seed", "holdout_nonce", "seed_protocol", "selection_bias_warning", "sources", "experiments", "interpretation", "report_sha256"}
    _keys(report, required)
    unsigned = {key: value for key, value in report.items() if key != "report_sha256"}
    if report["report_sha256"] != _sha(_canonical(unsigned)):
        raise ExperimentError("experiment report hash mismatch")
    manifest = validate_manifest(report["manifest"])
    if report["manifest_sha256"] != _sha(_canonical(manifest)):
        raise ExperimentError("experiment manifest hash mismatch")
    if report["status"] != "completed" or report["executor"] != "hashsmash-experiments-v1" or type(report["schema_version"]) is not int or report["schema_version"] != 1:
        raise ExperimentError("unsupported experiment report")
    if type(report["experiments"]) is not list or [r.get("id") for r in report["experiments"] if type(r) is dict] != [e["id"] for e in manifest["experiments"]]:
        raise ExperimentError("experiment report ids differ from manifest")
    for source in report["sources"]:
        _keys(source, {"path", "sha256", "size_bytes", "untrusted_source_text"})
        data = source["untrusted_source_text"].encode("utf-8")
        if source["sha256"] != _sha(data) or source["size_bytes"] != len(data):
            raise ExperimentError("experiment source hash mismatch")
    if {s["path"] for s in report["sources"]} != declared_files(manifest):
        raise ExperimentError("experiment report source set mismatch")
    return json.loads(_canonical(report))


def judge_view(report: Any) -> dict[str, Any]:
    """Return a bounded deterministic view of a trusted full report for a judge.

    Entire source and hypothesis text is preserved or the view fails. Large raw
    pair and observation tables stay in the full report and are hash-bound. This
    is an evidence index with checked aggregate facts, not a proof certificate.
    """
    checked = verify_report_integrity(report)
    if sum(source["size_bytes"] for source in checked["sources"]) > 64 * 1024:
        raise ExperimentError("judge evidence source text exceeds the global 64-KiB review budget")
    view = {key: value for key, value in checked.items() if key not in {"report_sha256", "experiments"}}
    view["view_kind"] = "judge-evidence-view-v1"
    view["full_report_sha256"] = checked["report_sha256"]
    view["view_limitations"] = (
        "Full source text, manifest and summary statistics are included. Raw message pairs and numeric participant observations are omitted; at most three checked-trial previews and canonical table hashes are included. Consult the full trusted report for replay. Summaries do not establish algorithm cost, independent trials or extrapolation."
    )
    entries = []
    for entry in checked["experiments"]:
        compact = {key: value for key, value in entry.items() if key != "checked_trials"}
        if "checked_trials" in entry:
            rows = entry["checked_trials"]
            compact["checked_trials_sha256"] = _sha(_canonical(rows))
            compact["checked_trial_summary"] = {
                "rows": len(rows),
                "returned_pairs": sum("pair_sha256" in row for row in rows),
                "full_collisions": sum(row.get("full_collision") is True for row in rows),
                "repeated_pairs": sum(row.get("repeated_pair") is True for row in rows),
                "no_pair_returned": sum(row.get("reason") == "no_pair_returned" for row in rows),
            }
            observations = [{"trial": row["trial"], "observations": row["untrusted_participant_observations"]} for row in rows if "untrusted_participant_observations" in row]
            compact["untrusted_observation_summary"] = {
                "rows": len(observations),
                "values": sum(len(row["observations"]) for row in observations),
                "sha256": _sha(_canonical(observations)),
                "trust": "untrusted_participant_numbers; not used in host success or cost accounting",
            }
            preview = []
            for row in rows[:3]:
                preview.append({key: value for key, value in row.items() if key not in {"message_a_hex", "message_b_hex", "untrusted_participant_observations"}})
            compact["checked_trial_preview"] = preview
        entries.append(compact)
    view["experiments"] = entries
    view["view_sha256"] = _sha(_canonical(view))
    if len(_canonical(view)) > 256 * 1024:
        raise ExperimentError("judge evidence view exceeds its 256-KiB review budget")
    return view
