#!/bin/bash

set -e

# Check if folder name is passed
if [ -z "$1" ]; then
  echo "Usage: $0 <type-of-service>"
  echo "Example: $0 llm-gateway"
  exit 1
fi

FOLDER_NAME=$1
DOCKERFILE_DIR="./$FOLDER_NAME"

# Validate Dockerfile exists
if [ ! -f "$DOCKERFILE_DIR/Dockerfile" ]; then
  echo "❌ No Dockerfile found in $DOCKERFILE_DIR"
  exit 1
fi

# Compose image name
IMAGE_NAME="subhomoy/homelab-${FOLDER_NAME}-service"
TAG=$(date +"%Y%m%d%H%M%S")

echo "[+] Building image: $IMAGE_NAME:$TAG from $DOCKERFILE_DIR..."
docker build -t "$IMAGE_NAME:$TAG" "$DOCKERFILE_DIR"

echo "[+] Tagging image as latest..."
docker tag "$IMAGE_NAME:$TAG" "$IMAGE_NAME:latest"

echo "[+] Pushing image: $IMAGE_NAME:$TAG"
docker push "$IMAGE_NAME:$TAG"

echo "[+] Pushing image: $IMAGE_NAME:latest"
docker push "$IMAGE_NAME:latest"

echo "[+] Finished ✅"
