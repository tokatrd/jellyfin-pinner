"""Smoke: mismatch=1, match=0, unknown/missing=2. Uses temp files, not the repo dir."""

import os, json, subprocess, pathlib, tempfile

os.chdir(pathlib.Path(__file__).parent)

tmp = pathlib.Path(tempfile.mkdtemp())
try:
    (tmp / "mis.json").write_text('{"intro_skipper": "0.1.16.0"}')
    r = subprocess.run(
        ["python3", "pinner.py", "10.9.11", str(tmp / "mis.json")],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 1 and "PIN intro_skipper" in r.stdout, (
        r.returncode,
        r.stdout,
    )

    (tmp / "ok.json").write_text('{"intro_skipper": "0.1.18.0"}')
    r = subprocess.run(
        ["python3", "pinner.py", "10.9.11", str(tmp / "ok.json")],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0 and "OK intro_skipper" in r.stdout, (
        r.returncode,
        r.stdout,
    )

    r = subprocess.run(
        ["python3", "pinner.py", "11.0.0", str(tmp / "ok.json")],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 2 and "WARN" in r.stdout, (r.returncode, r.stdout)

    r = subprocess.run(
        ["python3", "pinner.py", "10.9.11", str(tmp / "nope.json")],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 2 and "ERROR" in r.stderr, (r.returncode, r.stderr)

    r = subprocess.run(
        ["python3", "pinner.py", "10.9.11", str(tmp / "ok.json")],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0
    print("jellyfin-pinner smoke OK")
finally:
    for p in tmp.glob("*"):
        p.unlink()
    tmp.rmdir()
