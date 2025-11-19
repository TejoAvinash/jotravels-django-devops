#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$HOME/jotravels-django-devops"

echo "🚀 [1] Go to app directory"
cd "$APP_DIR"

echo "📥 [2] Pull latest code from GitHub"
git fetch origin main
git reset --hard origin/main

echo "🐳 [3] Stop old containers"
docker compose down --remove-orphans || true

echo "🔨 [4] Build new image"
docker compose build

echo "▶ [5] Start app with docker-compose"
docker compose up -d

echo "🩺 [6] Health check"
sleep 8

if curl -fsS http://localhost:8000/ > /dev/null 2>&1; then
  echo "✅ Deployment successful."
else
  echo "❌ FAILED – check logs"
  docker compose logs --tail=50
  exit 1
fi
