#!/bin/bash
set -e

echo "🚀 JoTravels Deployment Starting..."

# 1) Go to app directory
cd /home/ubuntu/jotravels-django-devops || exit
echo "📁 Directory changed"

# 2) Pull latest code
echo "⬇️ Pulling latest code from GitHub..."
git pull origin main

# 3) Stop old container (if exists)
echo "🛑 Stopping old container..."
sudo docker stop jotravels || true
sudo docker rm jotravels || true

# 4) Ensure persistent DB folder exists
echo "📦 Checking persistent database folder..."
mkdir -p /home/ubuntu/jotravels-data

# 5) Build new image
echo "🐳 Building new Docker image..."
sudo docker build -t jotravels .

# 6) Run new container with persistent volume
echo "🚀 Starting new container..."
sudo docker run -d \
    --name jotravels \
    --env-file .env \
    -p 8000:8000 \
    -v /home/ubuntu/jotravels-data:/app \
    jotravels

# 7) Restart Nginx
echo "🔁 Restarting Nginx..."
sudo systemctl restart nginx

echo "✅ Deployment completed successfully!"
