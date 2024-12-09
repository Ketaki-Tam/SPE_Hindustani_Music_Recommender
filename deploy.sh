#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Building backend Docker image..."
docker build -t backend-image .

echo "Building frontend Docker image..."
cd frontend
docker build -t frontend .
cd ..

echo "Tagging Docker images..."
docker tag backend-image:latest ketakitam/backend-image:latest
docker tag frontend:latest ketakitam/frontend:latest

echo "Pushing Docker images to Docker Hub..."
docker push ketakitam/backend-image:latest
docker push ketakitam/frontend:latest

echo "Applying Kubernetes deployment configuration..."
kubectl apply -f kubernetes-deployment.yaml

echo "Deployment completed successfully!"

