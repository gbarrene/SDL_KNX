#!/bin/bash
# Setup a new raspberry pi jessie (not lite) for using the KNX, Amazon Echo library
# 

#sudo apt-get update
#sudo apt-get upgrade

sudo apt-get install python3-picamera
sudo apt-get install python3-pip

sudo su
# as sudo user:

pip install -U pip setuptools
pip3 install flask-ask
pip3 install knxip
pip3 install paho-mqtt

exit

