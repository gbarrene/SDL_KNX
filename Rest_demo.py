from flask import Flask, redirect, url_for, escape, request, jsonify
import src.knx_bus_SDL as sdl_knx
import src.constants as constants
import threading

app = Flask(__name__)
tunnel = sdl_knx.KNX_tunnel('192.168.1.99')
animation = sdl_knx.Animation(tunnel)


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
    return "All lights were set successfully"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
