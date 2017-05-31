# SDL_KNX
Swisscom Digital Lab KNX controller

Python code to control the KNX lights in the lab

## Hardware:

- Raspberry pi 3 B (https://www.digitec.ch/fr/s1/product/raspberry-pi-3-model-b-armv8-entwicklungsboards-kits-5704269)
- Micro SD card from Transcend (https://www.digitec.ch/fr/s1/product/transcend-microsdhc-premium-400x-mit-adapter-16go-class-10-cartes-memoires-3520393?tagIds=520)
- You will need also a ssh client as putty (https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html).

## Install procedure

You chould use the `Python_install_setup.sh` to have all modules use in this program.

- Install Rasbian Jessie Download from the raspberrypi web site. Download the normal version not the lite one. (https://downloads.raspberrypi.org/raspbian_latest)
- Burn the image file into the sd card with rufus ou win32diskimager. (https://sourceforge.net/projects/win32diskimager/)
- Creat an empty file without any extention called `ssh` in the boot sd card.
- Insert the sd card into the pi and boot it up.
- Search for the pi ip address on your router and connect to it.
- Log in with the pi user. (by default it is "pi" as a username and "raspberry" as a password)
- Go to the /home/pi/Documents directory in the shell.
- Make sure to be connected to the internet of the lab and to have the right tomezone setted.
- Clone the repository `git clone https://github.com/gbarrene/SDL_KNX.git`and enter into the repository `cd SDL_KNX`.
- Use the command `bash Python_install_setup.sh` to launch all the instalation process. It will update the pi, install all the program needed and launch the applications. It may take a near an hour or so.
- Go in your router settings on a web browser on (192.168.1.1) and set a fixed local IP for the pi. You need to redirect the port where the lora http requests are send (see in https://portal.lpn.swisscom.ch/deviceManager/ on which port you send the data) to the port 1880 of the pi for the sensor info to be received). If you need to restart the pi for ip change, do so with `sudo reboot` and reconnect to the pi. 
Use:
 `screen -S lights`
 `screen -d lights`
 `screen -dr lights`
 `cd /home/pi/Documents/SDL_KNX`
 `sudo python3 Light_flask_api.py` to restart the python app.
- Now go to your web browser and type in **_raspberrypi IP_**:1880/ui and you should end on an interface to control the lights.


## Install list:
### Python Modules List:
- KNX.ip
- Flask

### Node-Red node list:
- Dashboard
- MySQL
- PM2 to monitor the node red instant

## On system reboot or crashed:

If something goes wrong, Make sure that the pm2 service is working `pm2 info node-red`. If it is stopped or crashed, use `pm2 stop node-red` and then `pm2 start node-red`.

The python flask api schould be launch in a "screen" to be able to start and stop even with shell closed. This app must be **_started manually_**.

For exemple:
 `screen -S lights`
 `screen -d lights`
 `screen -dr lights`
 `cd /home/pi/Documents/SDL_KNX`
 `sudo python3 Light_flask_api.py`
 
## KNX Lights
"REST" API with Flask to control the lighting of the lab.
For the request list go to https://github.com/gbarrene/SDL_KNX/wiki/Request-list

## MQTT Thingdust
Read Thingdust MQTT messages and return where there is movement in the lab.

Use the `thingdust_demo.py` is you want to activate the light in wikihouse 1 and 2 just by moving inside.

