#!/bin/bash

# Prompt the user for input
read -p "Enter the host (default: 127.0.0.1): " host
host=${host:-127.0.0.1}
read -p "Enter the port (default: 3306): " port
port=${port:-3306}
read -p "Enter the user: " user
read -p "Enter the password: " password

# Check if user and password are empty
if [[ -z $user || -z $password ]]; then
    echo "Error: User and password must be provided!"
    exit 1
fi

echo "Setting up the database..."

# Update the server_config.json file
sed -i "s/\"host\": \".*\"/\"host\": \"$host\"/" database/server_config.json
sed -i "s/\"port\": \".*\"/\"port\": \"$port\"/" database/server_config.json
sed -i "s/\"user\": \".*\"/\"user\": \"$user\"/" database/server_config.json
sed -i "s/\"password\": \".*\"/\"password\": \"$password\"/" database/server_config.json

# Updata the fis_config.json file
sed -i "s/\"host\": \".*\"/\"host\": \"$host\"/" database/fis_config.json
sed -i "s/\"port\": \".*\"/\"port\": \"$port\"/" database/fis_config.json
sed -i "s/\"user\": \".*\"/\"user\": \"$user\"/" database/fis_config.json
sed -i "s/\"password\": \".*\"/\"password\": \"$password\"/" database/fis_config.json

echo "Setup completed!"