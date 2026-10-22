"""Canonical POC output and atomic publication (not frozen scientific output)."""
import hashlib
import json
import os
import uuid
from pathlib import Path


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def publish_immutable(destination: Path, data: bytes) -> None:
    """Windows: os.rename refuses to overwrite an existing destination.

    This no-clobber property MUST be tested under Windows (not assumed on POSIX).
    Status files, unlike predictions, may be updated with os.replace.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise FileExistsError(f"POC result already exists: {destination}")
    temporary = destination.with_name(destination.name + ".part-" + uuid.uuid4().hex)
    try:
        with temporary.open("xb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.rename(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def publish_mutable_status(destination: Path, content: dict) -> None:
    """A status file may legitimately progress STARTED -> SUCCESS / FAILED."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".part-" + uuid.uuid4().hex)
    try:
        with temporary.open("xb") as f:
            f.write(canonical_json(content))
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
