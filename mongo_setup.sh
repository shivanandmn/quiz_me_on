## install in wsl:https://dev.to/arielro85/install-mongodb-on-wsl2-and-ubuntu2204-33j4
## https://www.mongodb.com/developer/products/mongodb/mongodb-on-raspberry-pi/
sudo apt-get install gnupg
curl -fsSL https://pgp.mongodb.com/server-6.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg \
   --dearmor

echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list


sudo apt-get update
sudo apt-get install -y mongodb-org
# mkdir -p data/db
# mongod --dbpath data/db
# Ensure mongod config is picked up:
sudo systemctl daemon-reload

# Tell systemd to run mongod on reboot:
sudo systemctl enable mongod

# Start up mongod!
sudo systemctl start mongod

# $ sudo systemctl status mongod