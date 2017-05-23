import paho.mqtt.client as mqtt
import json

# Constants
# list of sensors from the Digital Lab
DSL_motion_sensors = [['A81758FFFE03045F', 'Reception'],
                      ['A81758FFFE030460', 'VR_corner'],
                      ['A81758FFFE030461', 'Squad_3'],
                      ['A81758FFFE030425', 'Squad_2'],
                      ['A81758FFFE0303FC', 'Squad_1'],
                      ['A81758FFFE0301CC', 'Wiki_1'],
                      ['A81758FFFE0304B5', 'Wiki_2'],
                      ['A81758FFFE0304B7', 'Wiki_3']
                      ]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if str(rc):
        print("Connection successful")
    else:
        print("Connected failed with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/sensor/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = str(msg.payload)[2:]
    print(payload)
    light = ((payload).rpartition('"Light":')[2]).rpartition(',')[0]
    topic = msg.topic
    print(topic+" "+light)
    rcv_euid = str(msg.topic).split('/')[1]
    if rcv_euid in [row[0] for row in DSL_motion_sensors]:
        rcv_euid_index = [row[0] for row in DSL_motion_sensors].index(rcv_euid)
        print("SDL sensor motion detected." + " Location: " + DSL_motion_sensors[rcv_euid_index][1])
        print("Switching on lights...")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.10", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
