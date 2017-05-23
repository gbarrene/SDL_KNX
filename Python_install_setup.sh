#!/bin/bash
# Setup a new raspberry pi jessie (not lite) for using the KNX, Amazon Echo library
# 

sudo apt-get update
sudo apt-get upgrade
# as sudo user:

sudo apt-get install python3-picamera
sudo apt-get install python3-pip


sudo pip install -U pip setuptools
sudo pip3 install flask
sudo pip3 install knxip

# Packages no longer used or not implemented yet
#sudo pip3 install flask-ask
#sudo pip3 install paho-mqtt

exit

