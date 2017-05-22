# SDL_KNX
Swisscom Digital Lab KNX controller

Python code to control the KNX lights in the lab

## Install

You chould use the `Python_install_setup.sh` to have all modules use in this program.
It will use python3!

### Modules List:
- KNX.ip
- Flask

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
	For a custom brightness, you need to send in the http-body, the light brightness for each color (R-G-B-W) 
	
	- `POST`: Set the light to the disired level where you specified the coordinates
	- `DELETE`: Turn off the lights in the specified position in the lab
	
- _/zone/_**_zone_name_**  
	Indicate the zone_name that you want to interact with. (wikihouse_1, squad_1, presentation, ...)
	For a custom brightness, you need to send in the http-body, the light brightness for each color (R-G-B-W) 
	
	- `POST`: Set the light to the disired level in the zone specified in the URL
	- `DELETE`: Turn off the lights in the zone
	


## MQTT Thingdust
Read Thingdust MQTT messages and return where there is movement in the lab.

Use the `thingdust_demo.py` is you want to activate the light in wikihouse 1 and 2 just by moving inside.

