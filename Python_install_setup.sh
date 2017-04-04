#!/bin/bash
# Setup a new raspberry pi jessie (not lite) for using the KNX, Amazon Echo library
# 

#sudo apt-get update
#sudo apt-get upgrade

sudo su
# as sudo user:

apt-get install python3-picamera
apt-get install python3-pip


pip install -U pip setuptools
pip3 install flask
pip3 install flask-ask
pip3 install knxip
pip3 install paho-mqtt

exit

