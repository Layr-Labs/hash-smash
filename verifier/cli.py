"""Command line entry point for local testing and GitHub Actions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .certificates import verify_certificates
from .errors import VerificationError
from .intake import validate_candidate
from .io import canonical_json_bytes, load_json_bytes
from .score import build_score


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m verifier")
    commands = parser.add_subparsers(dest="command", required=True)

    intake = commands.add_parser("intake", help="validate and register a candidate package")
    intake.add_argument("--candidate", required=True, type=Path)
    intake.add_argument("--output-dir", type=Path)

    certificates = commands.add_parser("certificates", help="check declared certificates")
    certificates.add_argument("--candidate", required=True, type=Path)
    certificates.add_argument("--output", type=Path)

    score = commands.add_parser("score", help="emit a Yukon score for an AI-qualified aggregate")
    score.add_argument("--candidate", required=True, type=Path)
    score.add_argument("--aggregate", required=True, type=Path)
    score.add_argument("--output", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        if arguments.command == "intake":
            result = validate_candidate(arguments.candidate, arguments.output_dir)
        elif arguments.command == "certificates":
            result = verify_certificates(arguments.candidate, arguments.output)
        else:
            try:
                aggregate_data = arguments.aggregate.read_bytes()
            except OSError as error:
                raise VerificationError(f"judge aggregate: could not read: {error}") from error
            aggregate = load_json_bytes(aggregate_data, "judge aggregate")
            result = build_score(arguments.candidate, aggregate, arguments.output)
        sys.stdout.buffer.write(canonical_json_bytes(result))
        return 0
    except VerificationError as error:
        print(f"verification failed: {error}", file=sys.stderr)
        return 2
    except OSError as error:
        print(f"verification infrastructure error: {error}", file=sys.stderr)
        return 3


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

