#!/usr/bin/env bash

sudo apt update
sudo apt install -y nginx

# If the install failed, stop here
if ! command -v nginx >/dev/null 2>&1; then
    echo "Nginx installation failed."
    exit 1
fi

echo "Nginx installed successfully."
