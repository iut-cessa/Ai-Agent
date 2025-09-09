#!/bin/bash
# Script to create htpasswd file for phpMyAdmin authentication
# Default credentials: admin/admin123

# Create htpasswd file with admin user
# Password: admin123
echo 'admin:$apr1$rKjbSl0h$7yVLVZ1WUfzWVU3c5O6VV1' > /etc/nginx/.htpasswd

echo "htpasswd file created with default credentials:"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "To add more users, use:"
echo "htpasswd /etc/nginx/.htpasswd newusername"
