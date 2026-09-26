"""Jellyfin plugin version pinner. Stdlib only."""

import json, sys

VERSION_MAP = {
    "10.8": {"intro_skipper": "0.1.16.0"},
    "10.9": {"intro_skipper": "0.1.18.0"},
    "10.10": {"intro_skipper": "0.2.x (non-intros build)"},
}
NOTES = "Android TV: use default web player for injected skip button, else enable auto-skip server-side."


def check(server_version, plugins):
    major = ".".join(server_version.split(".")[:2])
    expected = VERSION_MAP.get(major, {})
    actions = []
    for name, want in expected.items():
        have = plugins.get(name)
        if have != want:
            actions.append(f"PIN {name}: have={have} want={want}")
        else:
            actions.append(f"OK {name}=={want}")
    actions.append("NOTE: " + NOTES)
    return actions


if __name__ == "__main__":
    server = sys.argv[1] if len(sys.argv) > 1 else "10.9.11"
    plugfile = sys.argv[2] if len(sys.argv) > 2 else "plugins.sample.json"
    try:
        plugins = json.load(open(plugfile))
    except FileNotFoundError:
        plugins = {"intro_skipper": "0.1.16.0"}
    results = check(server, plugins)
    for a in results:
        print(a)
    sys.exit(1 if any(a.startswith("PIN") for a in results) else 0)
