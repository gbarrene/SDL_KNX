#!/bin/bash
# Setup a new raspberry pi jessie (not lite) for using the KNX and node-red
# 

sudo apt-get update
yes Y | sudo apt-get upgrade


sudo apt-get install python3-pip


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
node-red-start
^C
node-red-stop
hash -r
cd /home/pi/.node-red
sudo npm install node-red-dashboard
sudo systemctl enable nodered.service
node-red-start

sudo python3 Light_flask_api.py

exit

