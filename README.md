# IP — DuckDNS updater

Polls your external IP and updates a DuckDNS subdomain via HTTPS whenever it
changes. Runs as a Docker container on a always-on host (e.g. Raspberry Pi).

## Setup

```bash
cp .env.example .env
# fill in DUCKDNS_TOKEN and DUCKDNS_DOMAIN
```

## Run

```bash
docker compose up -d --build
```

Restarts automatically on reboot (`restart: unless-stopped`).

## Dev

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest test_ip.py -v
```

## Deploy to Pi workflow

```bash
# on Pi
git clone git@github.com:cboin1996/IP.git ~/proj/IP
cd ~/proj/IP
cp .env.example .env && vim .env   # add real token
docker compose up -d --build
docker compose logs -f             # verify first update
```

## Environment variables

| Variable | Default | Description |
| --- | --- | --- |
| `DUCKDNS_TOKEN` | required | DuckDNS account token |
| `DUCKDNS_DOMAIN` | required | Subdomain (without `.duckdns.org`) |
| `CHECK_INTERVAL_HOURS` | `1` | How often to check for IP changes |
| `FAULT_INTERVAL_HOURS` | `0.1667` | Retry interval when offline (~10 min) |
