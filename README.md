    # SDL_KNX
Swisscom Digital Lab KNX controller

Python code to control the KNX lights in the lab

##Install

You chould use the `Python_install_setup.sh` to have all modules use in this program.
It will use python3!

###Modules List:
- Paho MQTT
- KNX.ip
- Flask

##KNX Lights
"REST" API with Flask to control the lighting of the lab.

###Request List 'POST':
- _/connection_ 
  Creat the knx tunnel

- _/all_on_ 
  Turn on all the lights

- _/all_off_ 
  Turn off all the lights 

- _/all_rgb_on_ 
  Turn on all the RGB lights 

- _/all_rgb_off_ 
  Turn off all the RGB lights 

- _/animation/_**_animationName_**  
  Launch the animation if it is define

##MQTT Thingdust
Read Thingdust MQTT messages and return where there is movement in the lab.

Use the `thingdust_demo.py` is you want to activate the light in wikihouse 1 and 2 just by moving inside.

