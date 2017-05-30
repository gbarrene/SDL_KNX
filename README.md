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
- Use the command `bash Python_install_setup.sh` to launch all the instalation process. It will update the pi, install all the program needed and launch the applications.
- Go in your router settings on a web browser on (192.168.1.1) and set a fixed local IP for the pi. It must be 192.168.1.10 for the node-red to be working. If you choose another one, you will need to change the url in the Node-Red node that do the http request.
- Now go to your web browser and type in 192.168.1.10:1880/ui and you should arrive on an interface to control the lights.


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
 `screen -dr lights`
 `cd /home/pi/Documents/SDL_KNX`
 `sudo python3 Light_flask_api.py`
 
## KNX Lights
"REST" API with Flask to control the lighting of the lab.

### Request List:
- _/connection_ 
	- `POST`: Creat the knx tunnel between the server running the code to the knx/ip gateway
	- `GET`: Return if the tunnel is opened or not

- _/all_on_ 
	- `POST`: Send a message to all the light to light up at 80%
	- `DELETE`: Turn off the lights

- _/all_off_ 
	- `POST`: Turn off the lights

- _/all_rgb_on_ 
	- `POST`: Send a message to all the RGB light to light up at 80%
	- `DELETE`: Turn off the lights

- _/all_rgb_off_ 
	- `POST`: Turn off the lights

- _/animation/_**_animationName_**  
	- `POST`: Launch the animation if it is define in the URL. Choose one that is implemented
	- `GET`: Retrun the name of the current animation running
	- `DELETE`: Stop the animation in the background

- _/position/_**_X;Y_**
	Coordinates must be in the lab map. See the map for position and axes.
	It changes lights in a radius around the position.
	For a custom brightness, you need to send in the http-body, the light brightness for each color (R-G-B-W) (EX: {"R": 27, "G": 255, "B":0, "W": 23})

	- `POST`: Set the light to the disired level where you specified the coordinates
	- `DELETE`: Turn off the lights in the specified position in the lab

- _/zone/_**_zone_name_**
	Indicate the zone_name that you want to interact with. (wikihouse_1, squad_1, presentation, ...)
	For a custom brightness, you need to send in the http-body, the light brightness for each color (R-G-B-W) (EX: {"R": 27, "G": 255, "B":0, "W": 23})

	- `POST`: Set the light to the disired level in the zone specified in the URL
	- `DELETE`: Turn off the lights in the zone

- _/active_light
	Set or clear the **_active-light_** bit. Active-light mode command the light brightness with the LORA sensor in the lab.

	- `POST`: Set the **_active-light_** bit
	- `DELETE`: Clear the **_active-light_** bit

- _/zone_light1/_**_zone_name_**
	Change the light level 1 of the selected zone
	The light level must be specified in the body in JSON formate (EX: {"light": 27})

	- `PUT`: Set the new light level in the file that contain the value dictionary

- _/zone_light2/_**_zone_name_**
	Change the light level 2 of the selected zone
	The light level must be specified in the body in JSON formate (EX: {"light": 27})

	- `PUT`: Set the new light level in the file that contain the value dictionary

- _/lora
	- `POST`: Only used for sending sensor data

## MQTT Thingdust
Read Thingdust MQTT messages and return where there is movement in the lab.

Use the `thingdust_demo.py` is you want to activate the light in wikihouse 1 and 2 just by moving inside.

