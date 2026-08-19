# Deploy Discovery

Use this reference when the deploy path is not obvious.

## What To Inspect

Search for:

- `package.json` scripts
- `Makefile`
- `docker-compose.yml` or `compose.yaml`
- `ecosystem.config.js`
- `systemd` service names in docs or scripts
- `deploy.sh`, `release.sh`, `restart.sh`
- CI workflows that mirror production rollout
- `README`, ops docs, or `.env.example` hints

## Discovery Questions

- Which branch or revision is supposed to be deployed?
- Which directory on the VPS holds the live app?
- Is the app deployed in-place, by release folders, or in containers?
- Which command rebuilds or installs dependencies?
- Which command restarts the service?
- Which health endpoint, page, or log proves startup worked?

## Selection Rule

Prefer the most explicit documented or scripted path. If multiple deployment methods exist, choose the one that matches the current environment and has the least ambiguity.
