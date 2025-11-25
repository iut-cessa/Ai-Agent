#!/bin/bash

# SSL Certificate Renewal Script for iut-aiagent.ir
# This script renews the Let's Encrypt certificate and reloads nginx

echo "Starting certificate renewal process..."

# Renew certificate
certbot renew --quiet

# Check if renewal was successful
if [ $? -eq 0 ]; then
    echo "Certificate renewed successfully"
    
    # Reload nginx in docker container
    docker exec nginx-proxy nginx -s reload
    
    if [ $? -eq 0 ]; then
        echo "Nginx reloaded successfully"
    else
        echo "Error: Failed to reload nginx"
        exit 1
    fi
else
    echo "Certificate renewal failed or not needed"
fi

echo "Certificate renewal process completed"
