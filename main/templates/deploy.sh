#!/bin/bash

echo "🚀 Starting JoTravels Deployment..."

cd /home/ubuntu/jotravels-django-devops || exit

sudo docker stop jotravels || true
sudo docker rm jotravels || true

git pull origin main

sudo docker build -t jotravels .
sudo docker run -d -p 8000:8000 --env-file .env --name jotravels jotravels

sudo systemctl restart nginx

echo "🎉 Deployment completed successfully!"
