"""Non-Windows source-level checks. NOT a substitute for Windows W-tests."""
import hashlib
import json
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    for name in ("Run_Experiment.bat", "install_upgrade_dependencies_into_venv.bat", "activate_venv.bat", "deactivate_venv.bat"):
        data = (root / name).read_bytes()
        assert b"\r\n" in data, name
        assert b"\n" not in data.replace(b"\r\n", b""), name
    assert (root / ".gitattributes").read_text().strip() == "*.bat text eol=crlf"
    sys.path.insert(0, str(root / "src" / "methods"))
    from _common.experiment_console_and_file_output import canonical_json, digest
    data = json.loads((root / "tests" / "fixtures" / "poc_canonical_fixture.json").read_bytes())
    assert data["values"] == [3, 1, 4, 1, 5, 9, 2, 6]
    assert sum(data["values"]) == 31
    one = canonical_json({"b": 2, "a": 1})
    two = canonical_json({"a": 1, "b": 2})
    assert one == two == b'{"a":1,"b":2}\n'
    assert digest(one) == hashlib.sha256(one).hexdigest()
    print("PASS: CRLF/Git policy, Python imports, canonical JSON fixture/digest")
    print("NOT TESTED: CMD batch execution, venv, pipe forwarding, Windows rename no-clobber")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
