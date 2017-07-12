import random

from flask import Flask, redirect, url_for, escape, request, jsonify
import src.knx_bus_SDL as sdl_knx
import src.constants as constants
import json
import src.file_WR as file_WR
import threading
from time import localtime, strftime

app = Flask(__name__)
tunnel = sdl_knx.KNX_tunnel('192.168.1.99')
animation = sdl_knx.Animation(tunnel)
active_light = 0


def restart():
    global app
    global tunnel
    app = Flask(__name__)
    tunnel = sdl_knx.KNX_tunnel('192.168.1.99')


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

    if request.method == 'POST':
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
    """Interaction with all the lights to turn them all on or off"""
    global tunnel
    if request.method == 'POST':
        sdl_knx.all_on(tunnel)
        return 'Successfully turned all the rgb led on'
    elif request.method == 'DELETE':
        sdl_knx.all_off(tunnel)
        return 'Successfully turned all the rgb led off'


@app.route('/all_off', methods=['POST'])
def all_off():
    """Interaction with all the lights to turn them all off"""
    global tunnel
    sdl_knx.all_off(tunnel)
    return 'Successfully turned all the rgb led off'


@app.route('/all_rgb_on', methods=['POST', 'DELETE'])
def all_rgb_on():
    """Interaction with all the RGB lights to turn them all on or off"""
    global tunnel
    if request.method == 'POST':
        sdl_knx.all_rgb_on(tunnel)
        return 'Successfully turned all the rgb led on'

    elif request.method == 'DELETE':
        sdl_knx.all_rgb_off(tunnel)
        return 'Successfully turned all the rgb led off'


@app.route('/all_rgb_off', methods=['POST'])
def all_rgb_off():
    """Interaction with all the RGB lights to turn them all off"""
    global tunnel
    sdl_knx.all_rgb_off(tunnel)
    return 'Successfully turned all the rgb led off'


@app.route('/animation/<string:animation_name>', methods=['POST', 'DELETE', 'GET'])
def animation_fonction(animation_name='test'):
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
def position(coordinates='0;0'):
    """Turns on/off light on a particular coordinate of the lab map
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

    '''maybe if not'''

    if sdl_knx.set_light_position(tunnel, x, y, color):
        return "Unable to write to the KNX bus"
    return "All lights were set successfully"


@app.route('/zone/<string:zone_name>', methods=['POST', 'DELETE'])
def zone(zone_name='0_0'):
    """Turns on/off lights in the zone name. If the zone name is more generic, it selects all
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
        restart()
        return "Unable to write to the KNX bus"
    else:
        return "All lights were set successfully"


@app.route('/zone_test/<string:zone_name>', methods=['POST', 'DELETE'])
def zone_test(zone_name='0_0'):
    """Test of the raspberry resistance"""
    global tunnel
    while True:
        if request.method == 'POST':
            random_brightness = random.randint(0, 255)
            color = [0, 0, 0, random_brightness]
            print(random_brightness)
        if sdl_knx.set_light_zone(tunnel, zone_name, color):
            return "Unable to write to the KNX bus"
        else:
            return "All lights were set successfully"


@app.route('/active_light', methods=['POST', 'DELETE'])
def active_light():
    """Enables to change the mode from non active light to active light and vice et versa
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


@app.route('/zone_light<string:num>/<string:zone_name>', methods=['PUT'])
def zone_light(zone_name='0_0', num='0'):
    """Updates, with PUT, the second light level of the light slope
    """
    if request.method == 'PUT':
        if request.json:
            zone_name = zone_name.upper()
            file_WR.RW_light_info_update(zone_name, 'light' + num, request.json['value'])
    return "light " + num + " from " + zone_name + " was updated to " + str(request.json['value'])


@app.route('/zone_light_threshold<string:num>/<string:zone_name>', methods=['PUT'])
def zone_light_threshold(zone_name='0_0', num='0'):
    """Updates, with PUT, the second light level of the light slope
    """
    if request.method == 'PUT':
        if request.json:
            zone_name = zone_name.upper()
            file_WR.RW_light_info_update(zone_name, 'light_threshold' + num, request.json['value'])
    return "light threshold " + num + " from " + zone_name + " was updated to " + str(request.json['value'])


@app.route('/lora', methods=['POST'])
def lora():
    global active_light
    print (active_light)
    global tunnel
    light_info_deveui = file_WR.RW_light_info_read()
    hour = int(strftime("%H", localtime()))

    if hour > 7 and hour < 20:
        if active_light:
            try:
                zone_name = light_info_deveui[request.json['DevEUI'].upper()]['zone_name']
                light1 = light_info_deveui[request.json['DevEUI'].upper()]['light1']
                light2 = light_info_deveui[request.json['DevEUI'].upper()]['light2']
                light_threshold1 = light_info_deveui[request.json['DevEUI'].upper()]['light_threshold1']
                light_threshold2 = light_info_deveui[request.json['DevEUI'].upper()]['light_threshold2']
                light_threshold3 = light_info_deveui[request.json['DevEUI'].upper()]['light_threshold3']
                brightness_level = light_info_deveui[request.json['DevEUI'].upper()]['brightness_level']
            except:
                return ("not found")

            if not zone_name == "0":
                if request.json['Light'] < light_threshold1:
                    brightness = light1
                elif request.json['Light'] < light_threshold2:
                    brightness = light2
                else:
                    brightness = int((((light2 / (light_threshold3 - light_threshold2)) * light_threshold3 + light2) -
                                      request.json['Light'] * (light2 / (light_threshold3 - light_threshold2))))

                if brightness < 0:
                    brightness = 0
                elif brightness > 255:
                    brightness = 255

                if zone_name[:4].upper() == "WIKI":
                    motion_data = file_WR.RW_motion_data_update(zone_name, request.json['Motion'])

                    if motion_data[zone_name.upper()]['last-7'] or motion_data[zone_name.upper()]['last-6'] or \
                            motion_data[zone_name.upper()]['last-5'] or motion_data[zone_name.upper()]['last-4'] or \
                            motion_data[zone_name.upper()]['last-3'] or motion_data[zone_name.upper()]['last-2'] or \
                            motion_data[zone_name.upper()]['last-1'] or motion_data[zone_name.upper()]['last']:
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

    file_WR.RW_light_info_write(light_info_deveui)
    return "Good"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
