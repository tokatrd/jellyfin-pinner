"""Smoke: mismatch exits 1, match exits 0."""

import os, subprocess, pathlib

os.chdir(pathlib.Path(__file__).parent)


r = subprocess.run(["python3", "pinner.py", "10.9.11", "plugins.sample.json"])
assert r.returncode == 1, "expected mismatch for 10.9 vs 0.1.16.0"
match = pathlib.Path("plugins.match.json")
match.write_text('{"intro_skipper": "0.1.18.0"}')
try:
    r2 = subprocess.run(["python3", "pinner.py", "10.9.11", "plugins.match.json"])
    assert r2.returncode == 0, "expected match for 10.9 vs 0.1.18.0"
finally:
    match.unlink()
print("jellyfin-pinner smoke OK")
