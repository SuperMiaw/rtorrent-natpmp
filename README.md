rtorrent-natpmp
===============

Enable NAT-PMP for rtorrent on the fly.

## Action performed
1. Request port forward to gateway.
2. Update rtorrent listening TCP port.
3. (if enabled) Enable DHT and setup UDP port.
4. Rebind rtorrent listening sockets
5. Refresh regulary port forwarding rule to keep it enabled (default: 45 seconds).

## Requirement
- rtorrent SCGI enabled and accessible through a webserver (nginx, apache, ...)

## Setup

Current project rely on `uv` for dependency management.

Quick-start
```sh
# Fetch dependencies
uv sync
# Copy and customize settings
cp conf/app.json.sample conf/app.json
# Run application
python3 -m app
```

Additional resources are provided in `deploy` folder to run script under `venv` as a service on freebsd.

## Development

This project require use of `pre-commit` for code quality checks.