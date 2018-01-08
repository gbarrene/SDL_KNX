import datetime
import random

from flask import Flask, redirect, url_for, escape, request, jsonify, render_template
import src.knx_bus_SDL as sdl_knx
import src.constants as constants
import json
import src.file_WR as file_WR
import threading
from time import localtime, strftime, sleep
from knxip.core import parse_group_address as toknx
app = Flask(__name__)
knx_gate = '62.203.241.102'
tunnel = sdl_knx.KNX_tunnel(knx_gate)
animation = sdl_knx.Animation(tunnel)
active_light_switch = 1


def restart():
    global app
    global tunnel
    app = Flask(__name__)
    tunnel = sdl_knx.KNX_tunnel(knx_gate)


@app.route('/')
def index():
    return render_template("index.html")  # 'Welcome on the SDL light API'


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
        sdl_knx.all_on(tunnel, 235)
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


@app.route('/test', methods=['POST'])
def test():
    print(request.POST['testValue'])
    return "done"
    # return "value"
    # zone_name = "presentation"
    # global tunnel
    # x= 0
    # if request.method == 'POST':
    #    while(x < 7):


#
#            brightness = random.randrange(0,200)
#            color = [int(request.json['R']), int(request.json['G']), int(request.json['B']), brightness]
#            x = x+1
#            if sdl_knx.set_light_zone(tunnel, zone_name, color):
#                restart()
#                return "Unable to write to the KNX bus"
# else:
# return "All lights were set successfully"
#        return "All lights were set successfully"


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


@app.route('/active/<string:zone_name>', methods=['POST', 'DELETE'])
def active_zone(zone_name='0_0'):
    global tunnel
    if request.method == 'POST':
        file_WR.RW_light_info_update(zone_name, 'active', 1)
        return "Active light activated in " + zone_name
    elif request.method == 'DELETE':
        file_WR.RW_light_info_update(zone_name, 'active', 0)
        return "Active light deactivated in " + zone_name


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


@app.route('/flic_zone/click/<string:zone_name>', methods=['POST'])
def flic_click_zone(zone_name='0_0'):
    global tunnel
    sensor_id = ""
    for line in constants.LORA_SENSOR:
        if zone_name in line:
            sensor_id = line[0]
    light_info_deveui = file_WR.RW_light_info_read()
    status = light_info_deveui[sensor_id]["flic_status"]
    if status == 0:
        color = [0, 0, 0, 235]
        file_WR.RW_light_info_update(zone_name, 'flic_status', 1)
    else:
        color = [0, 0, 0, 0]
        file_WR.RW_light_info_update(zone_name, 'flic_status', 0)
    if sdl_knx.set_light_zone(tunnel, zone_name, color):
        restart()
        return "Unable to write to the KNX bus"
    else:
        return "All lights were set successfully"


@app.route('/flic_zone/hold/<string:zone_name>', methods=['POST'])
def flic_hold_zone(zone_name='0_0'):
    global tunnel
    light_info_deveui = file_WR.RW_light_info_read()
    sensor_id = ""
    for line in constants.LORA_SENSOR:
        if zone_name in line:
            sensor_id = line[0]
    light_info_deveui = file_WR.RW_light_info_read()
    status = light_info_deveui[sensor_id]["flic_status"]
    color = [0, 0, 0, 255]
    file_WR.RW_light_info_update(zone_name, 'flic_status', 1)
    if sdl_knx.set_light_zone(tunnel, zone_name, color):
        restart()
        return "Unable to write to the KNX bus"
    else:
        return "All lights were set successfully"


@app.route('/flic_global/click', methods=['POST'])
def flic_global():
    global tunnel
    light_info_deveui = file_WR.RW_light_info_read()
    global_status = light_info_deveui.get("global_flic")
    if global_status == 0:
        sdl_knx.all_on(tunnel, 235)
        light_info_deveui['global_flic'] = 1
        for line in light_info_deveui:
            if type(light_info_deveui.get(line)) == type(light_info_deveui):
                light_info_deveui[line]["flic_status"] = 1
    else:
        sdl_knx.all_off(tunnel)
        light_info_deveui['global_flic'] = 0
        for line in light_info_deveui:
            if type(light_info_deveui.get(line)) == type(light_info_deveui):
                light_info_deveui[line]["flic_status"] = 0






@app.route("/flic_test", methods=['POST'])
def flic_test():
    light_info_deveui = file_WR.RW_light_info_read()
    sensor_id = 'A81758FFFE030461'
    status = light_info_deveui[sensor_id]["flic_status"]
    if status == 1:
        addresses = [['14/2/41', 1, 0],
                     ['14/2/46', 1, 0],
                     ['14/3/81', 4, 0],
                     ['14/3/101', 4, 0],
                     ['14/3/121', 4, 190],
                     ['14/3/141', 4, 190],
                     ['14/3/161', 4, 230],
                     ['14/3/181', 4, 230],
                     ['14/3/201', 4, 230],
                     ['14/3/221', 4,230]]
        for add in addresses:
            if add[1] == 1:
                if sdl_knx.set_led(tunnel, toknx(add[0]), add[2]):
                    print('1')
                    return 1
            else:
                if sdl_knx.set_rgb(tunnel, toknx(add[0]), [0, 0, 0, add[2]]):
                    print('1')
                    return 1
        file_WR.RW_light_info_update('presentation', 'flic_status', 0)
        return "All lights"
    else:
        zone_name = "presentation"
        color = [0, 0, 0, 253]
        file_WR.RW_light_info_update('presentation', 'flic_status', 1)
        if sdl_knx.set_light_zone(tunnel, zone_name, color):
            restart()
            return "Unable to write to the KNX bus"
        else:
            return "All lights were set successfully"


@app.route('/flic_presentation/hold', methods=['POST'])
def flic_presentation_hold():
    zone_z = 'PRESENTATION_'
    section = ['C', 'D', 'E', 'F', 'G', 'H', 'X', 'Y', 'A', 'B']
    file_WR.RW_light_info_update('presentation', 'flic_status', 0)
    for sec in section:
        global tunnel
        if sec in ['X', 'A', 'Y', 'B']:
            zone_name = zone_z + sec
            color = [0, 0, 0, 240]
            if sdl_knx.set_light_zone(tunnel, zone_name, color):
                restart()
                return "Unable to write to the KNX bus"
                # else:
                #    return "All lights were set successfully"
        if sec in ['C', 'D']:
            zone_name = zone_z + sec
            color = [0, 0, 0, 200]

            if sdl_knx.set_light_zone(tunnel, zone_name, color):
                restart()
                return "Unable to write to the KNX bus"
                # else:
                #   return "All lights were set successfully"
        else:
            zone_name = zone_z + sec
            color = [0, 0, 0, 0]

            if sdl_knx.set_light_zone(tunnel, zone_name, color):
                restart()

                return "Unable to write to the KNX bus"
                # else:
                #   return "All lights were set successfully"
    return "All lights were set successfully"


@app.route('/lora', methods=['POST'])
def lora():
    """
    This methods handle every messages sent by the LORA sensors and is also respoonsible of automatic lightning



    :return:
    """
    global active_light_switch
    global tunnel
    light_info_deveui = file_WR.RW_light_info_read()
    hour = int(strftime("%H", localtime()))
    day = datetime.datetime.today().weekday()
    lowerbound = 290
    upperbound = 500
    # we suppose that there is no need for light between 21 and 6 and during the weekend
    # however the active switch button is deactivated after the first all_off call to prevent
    # automatic turn off if somebody is working on the week-end or after 21h for example
    if hour < 7 or hour > 20 or day == 7 or day == 6:
        if active_light_switch == 1:
            sdl_knx.all_off(tunnel)
            active_light_switch = 0
        return "Non Active Time"
    else:
        if active_light_switch == 0:
            sdl_knx.all_on(tunnel, 235)
            active_light_switch = 1

        active_light_switch = 1
        try:
            sensorID = request.json['DevEUI'].upper()
            active = light_info_deveui[sensorID]['active']
            zone_name = light_info_deveui[sensorID]['zone_name']
            sensor_model = light_info_deveui[sensorID]['sensor_model']
            current_brightness = light_info_deveui[sensorID]['brightness_level']
            captured_light = request.json['Light']
        except:
            return 'Unable to read the required parameters'
        if zone_name != 0 and active:
            # Only ERS sensor can detect motion if there is no motion for more than 14 min, turn off
            if sensor_model == 'ERS':
                motion_data = file_WR.RW_motion_data_update(zone_name, request.json['Motion'])
                if not motion(motion_data, zone_name):
                    sdl_knx.set_light_zone(tunnel, zone_name[0, 0, 0, 0])
                    file_WR.RW_light_info_update(zone_name, "brightness_level", 0)
                    return "No motion in the room light was turned off"

            if lowerbound < captured_light < upperbound:
                return "no adjustments needed"
            elif captured_light >= upperbound:
                if current_brightness != 0:
                    lower_bright = 3 * current_brightness / 4
                    if lower_bright < 70:
                        if not sdl_knx.set_light_zone(tunnel, zone_name, [0, 0, 0, 0]):
                            return "Artificial light turned off"

                    else:
                        delta = current_brightness - lower_bright
                        for x in range(1, int(delta), 5):
                            if not sdl_knx.set_light_zone(tunnel, zone_name, [0, 0, 0, current_brightness - x]):
                                sleep(4)
                        return "Decreasing the artificial light"
                return "Already no artificial light"
            # Here we will hardcode a value for the lights. A captured light below 100 is very dark so we will directly
            #  go to a 65% light
            elif captured_light < 80:
                if current_brightness == 210 or current_brightness == 230:
                    hardcoded_bright = 230
                else:
                    hardcoded_bright = 210  # correspond to 65% regarding the range 0-255
                if not sdl_knx.set_light_zone(tunnel, zone_name, [0, 0, 0, hardcoded_bright]):
                    return "The artificial light has been set to 65% "
                return " The system wasn't able to set the new brightness value"
            else:
                # if there is currently no artificial light and that the captured light is too low we should increase
                #  significantly the light therefore we start the incrementation at 50 to 120 as a base step
                if current_brightness == 0:
                    for x in range(50, 200, 7):
                        if not sdl_knx.set_light_zone(tunnel, zone_name, [0, 0, 0, x]):
                            sleep(4)
                    return "Artificial light has been activated"
                else:
                    # if there is already artificial light and that we are below the threshold we increase the light
                    # of 20%
                    if current_brightness >= 250:
                        return "Already fully lighted"
                    for x in range(current_brightness, min(int(current_brightness + 255 / 100 * 15), 255), 5):
                        if not sdl_knx.set_light_zone(tunnel, zone_name, [0, 0, 0, x]):
                            sleep(4)
                    return "Artificial light has been increased"
    return "Something"


def motion(motion_data, zone_name):
    """

    :param motion_data: data of the last 7 messages for the motion values
    :param zone_name: the name of the zone
    :return: Return true if there were at least one motion in the last 7 messages
             Return false if there were no motion in the last 7 messages
    """
    last = 'last-'
    tab = [last + repr(i) for i in range(0, 8)]
    for x in tab:
        if motion_data[zone_name.upper()][x] != 0:
            return True
    return False


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
