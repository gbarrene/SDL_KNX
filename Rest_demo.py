from flask import Flask, redirect, url_for, escape, request, jsonify
import src.knx_bus_SDL as sdl_knx
import threading

app = Flask(__name__)
tunnel = sdl_knx.KNX_tunnel('192.168.1.99')
animation = sdl_knx.Animation(tunnel)


@app.route('/')
def index():
    return 'You are not logged in'


@app.route('/connection', methods=['GET', 'POST', 'DELETE'])
def connection():
    """Connection of the server to the KNX interface"""
    global tunnel
    if request.method == 'GET':

        if tunnel.check_connection_state():
            return 'Tunnel already opened'
        else:
            return 'Tunnel not opened yet, or crashed. Please open it with a "PUT" on the same URL'

    elif request.method == 'PUT':
        if tunnel.connect():
            print('Tunnel opened')
            return 'Tunnel opened successfully'
        else:
            return 'Tunnel not opened successfully. Please retry'
    elif request.method == 'DELETE':
        if tunnel.check_connection_state():
            tunnel.diconnect()
            return 'Tunnel closed successfully'
        else:
            return 'No tunnel opened'


@app.route('/all_on', methods=['POST'])
def all_rgb_on():
    global tunnel
    sdl_knx.all_on(tunnel)
    return 'Successfully turned all the rgb led on'


@app.route('/all_off', methods=['POST'])
def all_rgb_off():
    global tunnel
    sdl_knx.all_off(tunnel)
    return 'Successfully turned all the rgb led off'


@app.route('/all_rgb_on', methods=['POST'])
def all_rgb_on():
    global tunnel
    sdl_knx.all_rgb_on(tunnel)
    return 'Successfully turned all the rgb led on'


@app.route('/all_rgb_off', methods=['POST'])
def all_rgb_off():
    global tunnel
    sdl_knx.all_rgb_off(tunnel)
    return 'Successfully turned all the rgb led off'


@app.route('/animation/<string:animation_name>', methods=['POST', 'DELETE'])
def animation_fonction(animation_name = 'test'):
    global animation
    if request.method == 'POST':
        if not animation.isAlive():
            animation.method_name = animation_name
            animation.start()
            return animation_name+' is active'

        elif animation.method_name == animation_name:
            return animation_name+' is already alive'
        else:
            animation.method_name = animation_name

    elif request.method == 'DELETE':
        if animation.isAlive():
            animation.stop()
            animation.join()
            return 'Animation stopped'

        else:
            return 'No animation was started'


#
# Turn on/off light on a particular coordinate of the lab map
#
@app.route('/position/<string:coordinates>', methods=['POST', 'DELETE'])
def position(coordinates = '0;0'):
    global tunnel
    # POST to turn on the light on a particular coordinate
    if request.method == 'POST':
        if not request.json:
            print('wrfwrfgrgrgwrrfwwrf')
            r = '0'
            g = '0'
            b = '0'
            w = '200'

        else:
            r = request.json['R']
            g = request.json['G']
            b = request.json['B']
            w = request.json['W']

    # DELETE to turn off the light on a particular coordinate
    elif request.method == 'DELETE':
        r = '0'
        g = '0'
        b = '0'
        w = '0'

    x = (coordinates.rpartition(';'))[0]
    y = (coordinates.rpartition(';'))[2]

    return 'You choose x = ' + x + ' , y = ' + y+'. With this RGB value ' + r+' '+g+' '+b+ ' '+w


@app.route('/led/<string:number>', methods=['PUT'])
def led(number='0;0'):
    global tunnel
    r = request.json['R']
    g = request.json['G']
    b = request.json['B']
    w = request.json['W']

    x = (number.rpartition(';'))[0]
    y = (number.rpartition(';'))[2]

    return 'You choose x = ' + x + ' , y = ' + y+'. With this RGB value ' + r+' '+g+' '+b+ ' '+w


#
# @app.route('/led', methods=['GET', 'POST'])
# def led():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         return redirect(url_for('index'))
#     return '''<form action="" method="post"><p><input type=text name=username><p><input type=submit value=Login></form>'''
#

@app.route('/rgb', methods=['GET', 'POST'])
def rgb():
    return 'rgb'


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
