#!/usr/bin/env bash
#
# Repeatable deploy for the YIP prod stack on a single Linux host
# (e.g. a DigitalOcean droplet).
#
# Usage:
#   ./deploy.sh          # slim stack (no logging stack)
#   ./deploy.sh --loki   # include Loki + Promtail + Grafana (light, fits 4GB)
#   ./deploy.sh --elk    # include the ELK logging stack (needs ~8GB RAM)
#
set -euo pipefail

# Always run from the prod-stack directory.
cd "$(dirname "$0")"

APP_DIR="$(cd .. && pwd)"          # .../application
REPO_DIR="$(cd ../.. && pwd)"      # repo root (contains .git)

if [ ! -f .env ]; then
  echo "ERROR: prod-stack/.env not found." >&2
  echo "       Copy the template and fill in real values:" >&2
  echo "         cp .env.example .env && nano .env" >&2
  exit 1
fi

PROFILE_ARGS=()
for arg in "$@"; do
  case "$arg" in
    --elk)
      PROFILE_ARGS+=(--profile elk)
      echo "==> ELK profile enabled"
      ;;
    --loki)
      PROFILE_ARGS+=(--profile loki)
      echo "==> Loki/Grafana profile enabled"
      ;;
    *)
      echo "Unknown option: $arg (supported: --loki, --elk)" >&2
      exit 1
      ;;
  esac
done

echo "==> Pulling latest code (fast-forward only)"
git -C "$REPO_DIR" pull --ff-only || echo "   (skipped: not a clean fast-forward or not a git checkout)"

echo "==> Building the Angular front-end into webapp/yip/static/angular (Node 12 container)"
docker run --rm \
  -v "$APP_DIR/webapp:/app" \
  -w /app/yip-frontend \
  -e NODE_OPTIONS=--max_old_space_size=4096 \
  node:12 \
  bash -lc "npm install --no-audit --no-fund && node_modules/.bin/ng build --aot --output-path ../yip/static/angular --output-hashing=none"

echo "==> Ensuring the external Postgres volume exists"
docker volume inspect pg_data_volume >/dev/null 2>&1 || docker volume create pg_data_volume

echo "==> Building images and (re)starting the stack"
docker compose --env-file .env "${PROFILE_ARGS[@]}" up -d --build

echo ""
echo "==> Deploy complete. Current containers:"
docker compose --env-file .env "${PROFILE_ARGS[@]}" ps

echo ""
echo "First-time only: create the Django admin user with"
echo "  docker exec -it webapp python3 manage.py createsuperuser"
