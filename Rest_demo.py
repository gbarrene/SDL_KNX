from flask import Flask, redirect, url_for, escape, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return 'You are not logged in'


@app.route('/position/<string:coordinates>', methods=['PUT'])
def position(coordinates = '0;0'):
    r = request.json['R']
    g = request.json['G']
    b = request.json['B']
    w = request.json['W']

    x = (coordinates.rpartition(';'))[0]
    y = (coordinates.rpartition(';'))[2]

    return 'You choose x = ' + x + ' , y = ' + y+'. With this RGB value ' + r+' '+g+' '+b+ ' '+w

@app.route('//<string:coordinates>', methods=['PUT'])
def position(coordinates = '0;0'):
    r = request.json['R']
    g = request.json['G']
    b = request.json['B']
    w = request.json['W']

    x = (coordinates.rpartition(';'))[0]
    y = (coordinates.rpartition(';'))[2]

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
