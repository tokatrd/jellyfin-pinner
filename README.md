# jellyfin-pinner

I kept breaking my Jellyfin plugins on every server update (wrong plugin version for the server version), so here's the little checker I use now before upgrading.

**What it does:** `pinner.py` holds a version map (10.8/10.9/10.10+) and:
- reads a Jellyfin `plugins.json` / manifest listing,
- prints PIN / UPGRADE / ENABLE-AUTOSKIP actions per client (incl. the Android TV default-player note),
- exits non-zero on mismatch so cron/n8n can alert.

Stdlib only.

## Run
```bash
python3 pinner.py 10.9.11 plugins.sample.json
python3 test_pinner.py
```

*Put together with some AI help.*
