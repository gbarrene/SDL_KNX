import paho.mqtt.client as mqtt
import requests

# Constants
# list of sensors from the Digital Lab

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if str(rc):
        print("Connection successful")
    else:
        print("Connected failed with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/button/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = str(msg.payload).split("'")[1]
    payload = payload
    print(payload)
    topic = str(msg.topic)
    zone= (topic.split('/')[2])
    print('http://192.168.1.10:5000/zone/' + zone)
    if payload == '1':
        r = requests.post('http://192.168.1.10:5000/zone/' + zone)
    elif payload == '0':
        r = requests.delete('http://192.168.1.10:5000/zone/' + zone)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.10", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
