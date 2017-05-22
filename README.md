# SDL_KNX
Swisscom Digital Lab KNX controller

Python code to control the KNX lights in the lab

## Install

You chould use the `Python_install_setup.sh` to have all modules use in this program.
It will use python3!

### Modules List:
- Paho MQTT
- KNX.ip
- Flask

## KNX Lights
"REST" API with Flask to control the lighting of the lab.

### Request List 'POST':
-  _/connection_ 
	- `POST`: Creat the knx tunnel between the server running the code to the knx/ip gateway
	- `GET`: Return if the tunnel is opened or not 

-  _/all_on_ 
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
  Launch the animation if it is define

## MQTT Thingdust
Read Thingdust MQTT messages and return where there is movement in the lab.

Use the `thingdust_demo.py` is you want to activate the light in wikihouse 1 and 2 just by moving inside.

