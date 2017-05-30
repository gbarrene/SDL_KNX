#!/bin/bash
# Setup a new raspberry pi jessie (not lite) for using the KNX and node-red
# 

sudo apt-get update
yes Y | sudo apt-get upgrade


sudo apt-get install python3-pip
sudo apt-get install screen


sudo pip install -U pip setuptools
sudo pip3 install flask
sudo pip3 install knxip

# Packages no longer used or not implemented yet
#sudo pip3 install flask-ask
#sudo pip3 install paho-mqtt

#sudo apt-get install git
#cd ~/Documents
#sudo git clone https://github.com/gbarrene/SDL_KNX.git
yes Y | sudo apt-get install npm
sudo npm install -g npm@2.x 
sudo npm install -g pm2

pm2 start /usr/bin/node-red --node-args="--max-old-space-size=128" -- -v
pm2 save
pm2 startup systemd
pm2 stop /usr/bin/node-red

cp /home/pi/Documents/SDL_KNX/Node-Red/flows_raspberrypi.json /home/pi/.node-red
cp /home/pi/Documents/SDL_KNX/Node-Red/flows_raspberrypi_cred.json /home/pi/.node-red


hash -r
cd /home/pi/.node-red
sudo npm install node-red-dashboard
sudo npm install node-red-node-mysql
sudo systemctl enable ssh
sudo service ssh start

pm2 start /usr/bin/node-red --node-args="--max-old-space-size=128" -- -v

sudo python3 /home/pi/Documents/SDL_KNX/Light_flask_api.py


