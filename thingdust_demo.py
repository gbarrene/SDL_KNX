import paho.mqtt.client as mqtt
import src.knx_bus_SDL as sdl_knx
from knxip.core import parse_group_address as toknx
import time
import src.constants as constants


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if str(rc):
        print("Connection successful")
    else:
        print("Connected failed with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/sensor/pir/motion/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    rcv_euid = str(msg.topic).split('/')[4]
    if rcv_euid in [row[0] for row in constants.DSL_MOTION_SENSORS]:
        rcv_euid_index = [row[0] for row in constants.DSL_MOTION_SENSORS].index(rcv_euid)
        print("SDL sensor motion detected." + " Location: " + constants.DSL_MOTION_SENSORS[rcv_euid_index][1])
        if constants.DSL_MOTION_SENSORS[rcv_euid_index][1] is 'Wiki_1':
            print("Switching on lights Wiki 1")
            sdl_knx.setled(tunnel, toknx(constants.WIKIHOUSE_1), 255)
        if constants.DSL_MOTION_SENSORS[rcv_euid_index][1] is 'Wiki_2':
            print("Switching on lights Wiki 2")
            sdl_knx.setled(tunnel, toknx(constants.WIKIHOUSE_2), 255)
        #if constants.DSL_MOTION_SENSORS[rcv_euid_index][1] is 'Wiki_3':
        #    print("Switching on lights wiki 3")
        #    sdl_knx.setled(tunnel, toknx(constants.WIKIHOUSE_3), 255)


tunnel = sdl_knx.KNX_tunnel('192.168.1.99')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("sensobox.io", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
