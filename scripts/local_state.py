"""Per-track process exclusion and bounded-file run archives for local experiments."""

from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import uuid

from verifier.errors import VerificationError
from verifier.io import atomic_write_bytes, atomic_write_json


class TrackBusyError(VerificationError):
    pass


@contextmanager
def track_session(paths, command):
    if paths.track is None or command == "summary":
        yield {}
        return
    paths.work.mkdir(parents=True, exist_ok=True)
    with (paths.work / ".run.lock").open("a+b") as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise TrackBusyError(f"track {paths.track.id} is already running") from error
        started = datetime.now(timezone.utc)
        run_id = started.strftime("%Y%m%dT%H%M%S.%fZ") + "-" + uuid.uuid4().hex[:8]
        record = {"track_id": paths.track.id, "command": command,
                  "started_at": started.isoformat(), "run_id": run_id}
        try:
            yield record
        finally:
            archive = paths.reports / "runs" / run_id
            copied = []
            # Enumerated organizer outputs only: no candidate directory walk, .env,
            # provider credentials, or arbitrary user-selected files.
            for source in paths.generated:
                if source.is_file():
                    name = "score.json" if source == paths.score else source.name
                    atomic_write_bytes(archive / name, source.read_bytes())
                    copied.append(name)
            record["artifacts"] = copied
            record["finished_at"] = datetime.now(timezone.utc).isoformat()
            atomic_write_json(archive / "run.json", record)
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
