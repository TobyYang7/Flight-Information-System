#!/bin/bash

# Prompt the user for input
read -p "Enter the host (default: 127.0.0.1): " host
host=${host:-127.0.0.1}
read -p "Enter the port (default: 3306): " port
port=${port:-3306}
read -p "Enter the user: " user
read -s -p "Enter the password: " password

# Check if user and password are empty
if [[ -z $user || -z $password ]]; then
    echo "Error: User and password must be provided!"
    exit 1
fi

echo "Setting up the database..."

# Update the server_config.json and fis_config.json files
for json_file in database/server_config.json database/fis_config.json
do
    jq --arg host "$host" '.host = $host' $json_file > tmp.$$.json && mv tmp.$$.json $json_file
    jq --arg port "$port" '.port = $port' $json_file > tmp.$$.json && mv tmp.$$.json $json_file
    jq --arg user "$user" '.user = $user' $json_file > tmp.$$.json && mv tmp.$$.json $json_file
    jq --arg password "$password" '.password = $password' $json_file > tmp.$$.json && mv tmp.$$.json $json_file
done

echo "Setup configuration files completed."

python database/CREATE_DATABASE_FIS.py
python database/insert_data.py
