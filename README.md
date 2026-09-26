# jellyfin-pinner

I kept breaking my Jellyfin plugins on every server update (wrong plugin version for the server version), so here's the little checker I use now before upgrading.

## The input file

The checker reads a `{"plugin": "version"}` JSON file (`plugins.sample.json` shows the shape). Build yours from Jellyfin Dashboard → Plugins, or from `<jellyfin-data>/plugins/*/meta.json`. Add your own plugins to `VERSION_MAP` in `pinner.py` the same way.

## Run

```bash
python3 pinner.py 10.9.11 my-plugins.json
# PIN intro_skipper: have=0.1.16.0 want=0.1.18.0   (exit 1)
python3 test_pinner.py  # expect: jellyfin-pinner smoke OK
```

Exit codes: `0` = all pinned, `1` = mismatch, `2` = tool problem (unknown server, missing file). Handy for cron:

```cron
*/30 * * * * /usr/bin/python3 /opt/jellyfin-pinner/pinner.py 10.9.11 /opt/jellyfin-pinner/my-plugins.json || curl -fsS -m 10 -d "jellyfin plugin drift" https://n8n.example.com/webhook/alert
```

After a PIN: hold that plugin version (disable auto-update for it) or postpone the server upgrade until a matching build exists.

## Limitations

- Only tracks what's in `VERSION_MAP` (10.8/10.9/10.10 right now); unknown servers warn with exit 2.
- No verified IntroSkipper build for 10.10 yet — that prints SKIP, not OK.

Stdlib only (Python 3.8+). MIT — see LICENSE.

*Put together with some AI help.*
