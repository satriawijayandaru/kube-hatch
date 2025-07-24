#!/bin/bash

# Update package lists
sudo apt update

# Install PostgreSQL client
echo "Installing PostgreSQL client..."
sudo apt install -y postgresql-client

# Install MongoDB tools (includes mongodump and mongorestore)
echo "Installing MongoDB tools..."
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo gpg --dearmor -o /usr/share/keyrings/mongodb-server-6.0.gpg
echo "deb [signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | \
  sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install -y mongodb-database-tools

# Install esdump (Elasticsearch dump and restore tool via npm)
echo "Installing esdump via npm..."
if ! command -v npm &> /dev/null; then
  echo "Installing Node.js and npm..."
  sudo apt install -y nodejs npm
fi
sudo npm install -g elasticdump

echo "All tools installed successfully."
