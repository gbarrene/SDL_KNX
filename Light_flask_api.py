import datetime
import random

from flask import Flask, redirect, url_for, escape, request, jsonify
import src.knx_bus_SDL as sdl_knx
import src.constants as constants
import json
import src.file_WR as file_WR
import threading
from time import localtime, strftime, sleep

app = Flask(__name__)
tunnel = sdl_knx.KNX_tunnel('192.168.1.99')
animation = sdl_knx.Animation(tunnel)
active_light_switch = 0


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


# @app.route('/zone_test/<string:zone_name>', methods=['POST', 'DELETE'])
# def zone_test(zone_name='0_0'):
#     """Test of the raspberry resistance"""
#     global tunnel
#     while True:
#         if request.method == 'POST':
#             random_brightness = random.randint(0, 255)
#             color = [0, 0, 0, random_brightness]
#             print(random_brightness)
#         if sdl_knx.set_light_zone(tunnel, zone_name, color):
#             return "Unable to write to the KNX bus"
#         else:
#             return "All lights were set successfully"


@app.route('/active/<string:zone_name>', methods=['POST', 'DELETE'])
def active_zone(zone_name='0_0'):
    global tunnel
    if request.method == 'POST':
        file_WR.RW_light_info_update(zone_name, 'active', 1)
        return "Active light activated in " + zone_name
    elif request.method == 'DELETE':
        file_WR.RW_light_info_update(zone_name, 'active', 0)
        return "Active light desactivated in " + zone_name


@app.route('/active_light', methods=['POST', 'DELETE'])
def active_light():
    """Enables to change the mode from non active light to active light and vice et versa
    -Use POST to enable the active light mode which use the sensor brightness data to adapt the lights
    -Use DELETE to disable the active light mode"""
    global active_light_switch
    if request.method == 'POST':
        active_light_switch = 1
        print("active_light")
    elif request.method == 'DELETE':
        active_light_switch = 0
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
    global active_light_switch
    global tunnel
    light_info_deveui = file_WR.RW_light_info_read()
    hour = int(strftime("%H", localtime()))
    if 7 < hour < 20:
        if active_light_switch:
            try:
                zone_name = light_info_deveui[request.json['DevEUI'].upper()]['zone_name']
                light1 = light_info_deveui[request.json['DevEUI'].upper()]['light1']
                light2 = light_info_deveui[request.json['DevEUI'].upper()]['light2']
                light_threshold1 = light_info_deveui[request.json['DevEUI'].upper()]['light_threshold1']
                light_threshold2 = light_info_deveui[request.json['DevEUI'].upper()]['light_threshold2']
                light_threshold3 = light_info_deveui[request.json['DevEUI'].upper()]['light_threshold3']
                brightness_level = light_info_deveui[request.json['DevEUI'].upper()]['brightness_level']
            except:
                return "not found"

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
                            motion_data[zone_name.upper()]['last-1'] or motion_data[zone_name.upper()]['last-0']:
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


@app.route('/lora2', methods=['POST'])
def lora2():
    global active_light_switch
    global tunnel
    light_info_deveui = file_WR.RW_light_info_read()
    hour = int(strftime("%H", localtime()))
    day = datetime.datetime.today().weekday()
    lowerbound = 300
    upperbound = 650
    zone_name = 0
    # we suppose that there is no need for light between 21 and 6 and during the weekend
    # however the active switch button is deactivated after the first all_aff call to prevent
    # automatic turn off if somebody is working on the week end or after 21h for example
    if hour < 7 or hour > 20 or day == 7 or day == 6:
        if active_light_switch == 1:
            all_off()
            active_light_switch = 0
    else:
        active_light_switch = 1
        try:
            sensorID = request.json['DevEUI'].upper()
            active = light_info_deveui[sensorID]['active']
            #desired_bright = light_info_deveui[sensorID]['desired_brightness_bottom']
            zone_name = light_info_deveui[sensorID]['zone_name']
            sensor_model = light_info_deveui[sensorID]['sensor_model']
            current_brightness = light_info_deveui[sensorID]['brightness_level']
            captured_light = request.json['Light']
        except:
            return 'error'
        print (sensorID + ", " + current_brightness)
        if zone_name != 0 and active:
            # Only ERS sensor can detect motion if there is no motion for more than 14 min, turn off
            if sensor_model == 'ERS':
                motion_data = file_WR.RW_motion_data_update(zone_name, request.json['Motion'])
                if not motion(motion_data, zone_name):
                    if current_brightness == 0:
                        return "Already no lights"
                    sdl_knx.set_light_zone(tunnel, zone_name[0, 0, 0, 0])
                    file_WR.RW_light_info_update(zone_name, "brightness_level", 0)
                    return "No motion in the room "

            if lowerbound < captured_light < upperbound:
                return "no adjustments needed"
            elif captured_light >= upperbound:
                if current_brightness != 0:
                    lower_bright = 2 * current_brightness / 3
                    if lower_bright < 70:
                        if not sdl_knx.set_light_zone(tunnel, zone_name, [0, 0, 0, 0]):
                            file_WR.RW_light_info_update(zone_name, "brightness_level", 0)
                    else:
                        delta = current_brightness - lower_bright
                        for x in range(1, int(delta), 5):
                            if not sdl_knx.set_light_zone(tunnel, zone_name, [0, 0, 0, current_brightness + x]):
                                current_brightness += x
                                file_WR.RW_light_info_update(zone_name, "brightness_level", current_brightness)
                                sleep(4)
                        return "Decreasing the artificial light"
            # Here we will hardcode a value for the lights. A captured light below 100 is very dark so we will directly
            #  go to a 65% light
            elif captured_light < 100:
                hardcoded_bright = 166  # correspond to 65% regarding the range 0-255
                if not sdl_knx.set_light_zone(tunnel, zone_name, [0, 0, 0, hardcoded_bright]):
                    file_WR.RW_light_info_update(zone_name, "brightness_level", hardcoded_bright)
                    return "The artificial light has been set to 65% "
                return " The system wasn't able to set the new brightness value"
            else:
                # if there is currently no artificial light and that the captured light is too low we should increase
                #  significantly the light therefore we start the incrementation at 50 to 120 as a base step
                if current_brightness == 0:
                    for x in range(50, 120, 7):
                        if not sdl_knx.set_light_zone(tunnel, zone_name, [0, 0, 0, x]):
                            current_brightness = x
                            file_WR.RW_light_info_update(zone_name, "brightness_level", x)
                            sleep(3)
                    return "Artificial light has been activated"
                else:
                    # if there is already artificial light and that we are below the threshold we increase the light
                    # of 20%
                    for x in range(current_brightness, min(int(current_brightness + 255 / 100 * 20), 255)):
                        if not sdl_knx.set_light_zone(tunnel, zone_name, [0, 0, 0, x]):
                            current_brightness = x
                            file_WR.RW_light_info_update(zone_name, "brightness_level", current_brightness)
                            sleep(3)
                    return "Artificial light has been increased"
                    # #only the ERS sensor have a motion detection
                    # if sensor_model == 'ERS':
                    #     motion_data = file_WR.RW_motion_data_update(zone_name, request.json['Motion'])
                    #     if motion(motion_data,zone_name):
                    #
                    #         delta = desired_bright - captured_light
                    #         if captured_light < desired_bright:
                    #             brightness_to_add = delta/3
                    #             #new_bright = min(current_brightness, 66) + brightness_to_add  #hardcoded the "threshold for the lights"
                    #             new_bright = current_brightness +brightness_to_add
                    #             sdl_knx.set_light_zone(tunnel,zone_name,[0, 0, 0, new_bright])
                    #             file_WR.RW_light_info_update(zone_name, "brightness_level", new_bright)
                    #
                    #         elif abs(delta) > 300:
                    #
                    #         elif abs(delta) > 200:
                    #
                    #         elif abs(delta) > 100:
                    #
                    #         else:
                    #
                    #
                    #     else:
                    #         sdl_knx.set_light_zone(tunnel,zone_name, [0, 0, 0, 0])
                    #         file_WR.RW_light_info_update(zone_name, "brightness_level", 0)
                    # elif sensor_model == 'ESM5k':


def set_and_write_brightness(zone_name: str, new_bright: int) -> bool:
    if not sdl_knx.set_light_zone(tunnel, zone_name, [0, 0, 0, new_bright]):
        file_WR.RW_light_info_update(zone_name, "brightness_level", new_bright)
        return True
    return False


def motion(motion_data, zone_name):
    last = 'last-'
    tab = [last + repr(i) for i in range(0, 8)]
    for x in tab:
        if motion_data[zone_name.upper()][x] != 0:
            return True
    return False


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
