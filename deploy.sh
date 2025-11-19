#!/bin/bash
set -e

echo "🚀 JoTravels Deployment..."

# 1) Go to app directory
cd /home/ubuntu/jotravels-django-devops || exit

# 2) Pull latest code
echo "🔄 Pulling latest code from GitHub..."
git pull origin main

# 3) Stop old container (if exists)
echo "🛑 Stopping old container (if running)..."
sudo docker stop jotravels || true
sudo docker rm jotravels || true

# 4) Build new image
echo "🐳 Building new Docker image..."
sudo docker build -t jotravels .

# 5) Run new container
echo "🚀 Starting new container..."
sudo docker run -d \
  --name jotravels \
  --env-file .env \
  -p 8000:8000 \
  jotravels

# 6) Restart nginx
echo "🔁 Restarting nginx..."
sudo systemctl restart nginx

echo "✅ Deployment completed successfully!"
