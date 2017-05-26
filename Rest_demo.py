from flask import Flask, redirect, url_for, escape, request, jsonify
import src.knx_bus_SDL as sdl_knx
import src.constants as constants
import json
import threading
from time import localtime, strftime

app = Flask(__name__)
tunnel = sdl_knx.KNX_tunnel('192.168.1.99')
animation = sdl_knx.Animation(tunnel)
active_light = 0


@app.route('/')
def index():
    return 'Welcome on the SDL light API'


@app.route('/connection', methods=['GET', 'POST'])
def connection():

    """Connection of the server to the KNX interface"""
    global tunnel
    if request.method == 'GET':

        if tunnel.check_connection_state():
            return 'Tunnel already opened'
        else:
            return 'Tunnel not opened yet, or crashed. Please open it with a "POST" on the same URL'

    elif request.method == 'POST':
        if tunnel.connect():
            print('Tunnel opened')
            return 'Tunnel opened successfully'
        else:
            return 'Tunnel not opened successfully. Please retry'
    elif request.method == 'DELETE':
        if tunnel.check_connection_state():
            tunnel.disconnect()
            return 'Tunnel closed successfully'
        else:
            return 'No tunnel opened'


@app.route('/all_on', methods=['POST', 'DELETE'])
def all_on():
    global tunnel
    if request.method == 'POST':
        sdl_knx.all_on(tunnel)
        return 'Successfully turned all the rgb led on'
    elif request.method == 'DELETE':
        sdl_knx.all_off(tunnel)
        return 'Successfully turned all the rgb led off'


@app.route('/all_off', methods=['POST'])
def all_off():
    global tunnel
    sdl_knx.all_off(tunnel)
    return 'Successfully turned all the rgb led off'


@app.route('/all_rgb_on', methods=['POST', 'DELETE'])
def all_rgb_on():
    global tunnel
    if request.method == 'POST':
        sdl_knx.all_rgb_on(tunnel)
        return 'Successfully turned all the rgb led on'

    elif request.method == 'DELETE':
        sdl_knx.all_rgb_off(tunnel)
        return 'Successfully turned all the rgb led off'


@app.route('/all_rgb_off', methods=['POST'])
def all_rgb_off():
    global tunnel
    sdl_knx.all_rgb_off(tunnel)
    return 'Successfully turned all the rgb led off'


@app.route('/animation/<string:animation_name>', methods=['POST', 'DELETE', 'GET'])
def animation_fonction(animation_name = 'test'):

    """URL to launch/kill animation for the leds"""
    global animation
    if request.method == 'POST':
        if not animation.isAlive():
            animation.method_name = animation_name
            animation.start()
            return animation_name + " is active"

        elif animation.method_name == animation_name:
            return animation_name + " is already alive"

        else:
            animation.method_name = animation_name
            return animation_name + " is now active"

    elif request.method == 'DELETE':
        if animation.isAlive():
            animation.stop()
            animation.join()
            return "Animation stopped"

        else:
            return "No animation was started"
    elif request.method == 'GET':
        return animation.method_name + " is running"


@app.route('/position/<string:coordinates>', methods=['POST', 'DELETE'])
def position(coordinates = '0;0'):

    """Turn on/off light on a particular coordinate of the lab map
    Coordinates must be x; y type. The radius will define the radius of lights that light up"""
    global tunnel
    if request.method == 'POST':
        if not request.json:
            color = [0, 0, 0, 200]
        else:
            color = [int(request.json['R']), int(request.json['G']), int(request.json['B']), int(request.json['W'])]

    elif request.method == 'DELETE':
        color = [0, 0, 0, 0]

    x = int((coordinates.rpartition(';'))[0])
    y = int((coordinates.rpartition(';'))[2])

    if sdl_knx.set_light_position(tunnel, x, y, color):
        return "Unable to write to the KNX bus"
    return "All lights were set successfully"


@app.route('/zone/<string:zone_name>', methods=['POST', 'DELETE'])
def zone(zone_name='0_0'):

    """Turn on/off lights in the zone name. If the zone name is more generic, it selects all
    lights with this generic name at the beginning"""
    global tunnel
    if request.method == 'POST':
        if not request.json:
            color = [0, 0, 0, 200]
        else:
            color = [int(request.json['R']), int(request.json['G']), int(request.json['B']), int(request.json['W'])]

    elif request.method == 'DELETE':
        color = [0, 0, 0, 0]

    if sdl_knx.set_light_zone(tunnel, zone_name, color):
        return "Unable to write to the KNX bus"
    else:
        return "All lights were set successfully"


@app.route('/active_light', methods=['POST', 'DELETE'])
def active_light():

    """Enable to change the mode from non active light to active light and vice et versa
    -Use POST to enable the active light mode which use the sensor brightness data to adapt the lights
    -Use DELETE to disable the active light mode"""
    global active_light
    if request.method == 'POST':
        active_light = 1
        print("active_light")
    elif request.method == 'DELETE':
        active_light = 0
        print("no active_light")
    return "active light"


@app.route('/zone_light1/<string:zone_name>', methods=['PUT'])
def zone_light1(zone_name='0_0'):

    """Update, with PUT, the first light level of the light slope
    """
    if request.method == 'PUT':
        if request.json:
            zone_name = zone_name.upper()
            file = open("Light_info_DevEUI.txt", 'r')
            light_info_deveui = json.load(file)
            file.close()
            for x in range(0, len(light_info_deveui)):
                if light_info_deveui[list(light_info_deveui.keys())[x]]['zone_name'].upper() == zone_name:
                    light_info_deveui[list(light_info_deveui.keys())[x]]['light1'] = request.json['light']
            file = open("Light_info_DevEUI.txt", 'w')
            file.write(json.dumps(light_info_deveui))
            file.close()
    return "light1 from "+zone_name+" was updated"


@app.route('/zone_light2/<string:zone_name>', methods=['PUT'])
def zone_light2(zone_name='0_0'):

    """Update, with PUT, the second light level of the light slope
    """
    if request.method == 'PUT':
        if request.json:
            zone_name = zone_name.upper()
            file = open("Light_info_DevEUI.txt", 'r')
            light_info_deveui = json.load(file)
            file.close()
            for x in range(0, len(light_info_deveui)):
                if light_info_deveui[list(light_info_deveui.keys())[x]]['zone_name'].upper() == zone_name:
                    light_info_deveui[list(light_info_deveui.keys())[x]]['light2'] = request.json['light']
            file = open("Light_info_DevEUI.txt", 'w')
            file.write(json.dumps(light_info_deveui))
            file.close()
    return "light2 from "+zone_name+" was updated"


@app.route('/lora', methods=['POST'])
def lora():
    global active_light
    global tunnel
    file = open("Light_info_DevEUI.txt", 'r')
    light_info_deveui = json.load(file)
    file.close()
    hour = int(strftime("%H", localtime()))
    motion = False

    if hour > 7 and hour < 20:
        if active_light:
            try:
                zone_name = light_info_deveui[request.json['DevEUI'].upper()]['zone_name']
                light1 = light_info_deveui[request.json['DevEUI'].upper()]['light1']
                light2 = light_info_deveui[request.json['DevEUI'].upper()]['light2']
                brightness_level = light_info_deveui[request.json['DevEUI'].upper()]['brightness_level']
            except:
                return ("not found")

            if not zone_name == "0":
                if request.json['Light'] < 350:
                    brightness = light1
                elif request.json['Light'] < 500:
                    brightness = light2
                else:
                    brightness = int((((light2 / 450)*500)+light2) - request.json['Light'] * (light2 / 450))

                if brightness < 0:
                    brightness = 0

                if zone_name[:4].upper() == "WIKI":
                    file = open("Motion_data.txt", 'r')
                    motion_data = json.load(file)
                    file.close()
                    motion_data[zone_name.upper()]['last-7'] = motion_data[zone_name.upper()]['last-6']
                    motion_data[zone_name.upper()]['last-6'] = motion_data[zone_name.upper()]['last-5']
                    motion_data[zone_name.upper()]['last-5'] = motion_data[zone_name.upper()]['last-4']
                    motion_data[zone_name.upper()]['last-4'] = motion_data[zone_name.upper()]['last-3']
                    motion_data[zone_name.upper()]['last-3'] = motion_data[zone_name.upper()]['last-2']
                    motion_data[zone_name.upper()]['last-2'] = motion_data[zone_name.upper()]['last-1']
                    motion_data[zone_name.upper()]['last-1'] = motion_data[zone_name.upper()]['last']
                    motion_data[zone_name.upper()]['last'] = request.json['Motion']
                    file = open("Motion_data.txt", 'w')
                    file.write(json.dumps(motion_data))
                    file.close()

                    if motion_data[zone_name.upper()]['last-7'] or motion_data[zone_name.upper()]['last-6'] or motion_data[zone_name.upper()]['last-5'] or motion_data[zone_name.upper()]['last-4'] or motion_data[zone_name.upper()]['last-3'] or motion_data[zone_name.upper()]['last-2'] or motion_data[zone_name.upper()]['last-1'] or motion_data[zone_name.upper()]['last']:
                        if brightness_level != brightness:
                            sdl_knx.set_light_zone(tunnel, zone_name, [0, 0, 0, brightness])
                            light_info_deveui[request.json['DevEUI'].upper()]['brightness_level'] = brightness
                        print(str(request.json['Light']) + "  " + str(brightness) + "  " + zone_name)
                    else:
                        if brightness_level != brightness:
                            sdl_knx.set_light_zone(tunnel, zone_name, [0, 0, 0, 0])
                            light_info_deveui[request.json['DevEUI'].upper()]['brightness_level'] = 0
                        print(str(request.json['Light']) + "  0  " + zone_name)

                else:
                    if brightness_level != brightness:
                        sdl_knx.set_light_zone(tunnel, zone_name, [0, 0, 0, brightness])
                        light_info_deveui[request.json['DevEUI'].upper()]['brightness_level'] = brightness
                    print(str(request.json['Light']) + "  " + str(brightness) + "  " + zone_name)
        else:
            for x in range(0, len(light_info_deveui)):
                light_info_deveui[list(light_info_deveui.keys())[x]]['brightness_level'] = 0

    file = open("Light_info_DevEUI.txt", 'w')
    file.write(json.dumps(light_info_deveui))
    file.close()
    return "Good"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
