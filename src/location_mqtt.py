import paho.mqtt.client as mqtt

# Constants
# list of sensors from the Digital Lab
DSL_motion_sensors = [['000070B3D5C1503F', 'Cofe'],
                      ['000070B3D5C15046', 'Squad_1'],
                      ['000070B3D5C15071', 'Squad_2'],
                      ['000070B3D5C15048', 'Squad_3'],
                      ['000070B3D5C15041', 'Squad_4'],
                      ['000070B3D5C15045', 'Wiki_1'],
                      ['000070B3D5C150FF', 'Wiki_2'],
                      ['000070B3D5C15043', 'Wiki_3'],
                      ['000070B3D5C15044', 'Homy'],
                      ['000070B3D5C15042', 'Tetris']
                      ]

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
    if rcv_euid in [row[0] for row in DSL_motion_sensors]:
        rcv_euid_index = [row[0] for row in DSL_motion_sensors].index(rcv_euid)
        print("SDL sensor motion detected." + " Location: " + DSL_motion_sensors[rcv_euid_index][1])

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("sensobox.io", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()