# VPS Deploy Patterns

Use this reference to match the deploy method to the actual stack.

## Git Working Tree + Process Manager

Common sequence:

1. SSH into the server
2. `cd` into the live project directory
3. fetch or pull the right branch
4. install dependencies if needed
5. build if needed
6. restart the process manager target
7. inspect logs or health endpoint

## PM2

Typical concerns:

- correct ecosystem file
- environment reload
- zero-downtime reload vs hard restart
- confirming the right app name

## systemd

Typical concerns:

- correct unit name
- daemon reload only when service files changed
- `systemctl restart` vs `reload`
- `journalctl` for immediate failure evidence

## Docker Compose

Typical concerns:

- right compose file
- image rebuild requirement
- service-specific restart
- container health and logs after up

## Shell Script Deploys

If the repo already has a deploy script, prefer it over retyping its steps manually. Inspect it first so you understand side effects, migrations, and restart behavior.
