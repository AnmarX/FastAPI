#!/bin/bash


# create .env file and two variables proxy(the url of the app) domain(ip of the VM or the domain)

# Read the domain name from domain.txt
domain=$(cat domain.txt)
proxy=$(cat proxy.txt)


sudo apt update
sudo apt install nginx

sudo apt install git-all

git clone https://github.com/AnmarX/FastAPI.git

env_file_path="./home/anmar/.env"

sudo mv "$env_file_path" "./home/anmar/FastAPI/full_stack_todo"

# Install Nginx


# Write Nginx configuration
sudo tee /etc/nginx/sites-available/myfastapiapp <<EOF
server {
    listen 80;
    server_name $domain;  # Use the domain read from domain.txt or IP address

    location / {
        proxy_pass $proxy;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Create a symbolic link to enable the site
sudo ln -s /etc/nginx/sites-available/myfastapiapp /etc/nginx/sites-enabled/

# Restart Nginx
sudo systemctl restart nginx


sudo apt-get update
sudo apt-get install ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin


cd FastAPI

cd full_stack_todo

sudo docker compose up --build

