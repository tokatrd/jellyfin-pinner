"""Check Jellyfin plugin versions against the server version. Stdlib only.

Exit codes (cron-friendly): 0 = all pinned, 1 = mismatch, 2 = tool problem
(unknown server, missing/unreadable file, unknown-good version).
"""

import json, sys

VERSION_MAP = {
    "10.8": {"intro_skipper": "0.1.16.0"},
    "10.9": {"intro_skipper": "0.1.18.0"},
    "10.10": {"intro_skipper": None},  # no verified build yet; check the plugin repo
}
NOTES = "Android TV: use the default web player for the injected skip button, else enable auto-skip server-side."


def check(server_version, plugins):
    major = ".".join(server_version.split(".")[:2])
    if major not in VERSION_MAP:
        return (
            2,
            [
                f"WARN: server {server_version} not in map (covers: {', '.join(sorted(VERSION_MAP))})"
            ],
        )
    actions, code = [], 0
    for name, want in VERSION_MAP[major].items():
        have = plugins.get(name, "(not installed)")
        if want is None:
            actions.append(
                f"SKIP {name}: no verified build for server {major} yet — check the plugin repo"
            )
            code = 2
        elif have != want:
            actions.append(f"PIN {name}: have={have} want={want}")
            code = 1
        else:
            actions.append(f"OK {name}=={want}")
    actions.append("NOTE: " + NOTES)
    return (code, actions)


if __name__ == "__main__":
    server = sys.argv[1] if len(sys.argv) > 1 else "10.9.11"
    plugfile = sys.argv[2] if len(sys.argv) > 2 else "plugins.sample.json"
    try:
        with open(plugfile) as f:
            plugins = json.load(f)
    except FileNotFoundError:
        print(
            f'ERROR: {plugfile} not found — pass your {{"plugin": "version"}} JSON file',
            file=sys.stderr,
        )
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"ERROR: {plugfile} is not valid JSON: {e}", file=sys.stderr)
        sys.exit(2)
    code, actions = check(server, plugins)
    for a in actions:
        print(a)
    sys.exit(code)
