#!/usr/bin/env bash
set -e

echo "Setting up Nginx..."

# Check if nginx is already installed by checking if the command exists
if command -v nginx >/dev/null 2>&1; then
    echo "Nginx is already installed."
    exit 0
fi

echo "updating package lists..."
sudo apt update

echo "installing nginx..."
sudo apt install -y nginx   

echo "nginx installed successfully."
