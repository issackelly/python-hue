#!/usr/bin/env python
from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, request
from flask.ext.socketio import SocketIO, emit
import random
import requests
import os
import json
from hue import Hue

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
app.debug = True
socketio = SocketIO(app)

resp = requests.get('https://www.meethue.com/api/nupnp')
ip = json.loads(resp.content)[0]["internalipaddress"]

h = Hue()
h.station_ip = ip
h.get_state()


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('update_light', namespace='/lights')
def message(message):
    print message
    h.lights[message["light"]].set_state(message["state"])

    h.get_state()
    emit('state', {'data': h.state}, broadcast=True)

@socketio.on('connect', namespace='/lights')
def connect():
    print message
    h.get_state()
    emit('state', {'data': h.state}, broadcast=True)



# Purple 57, 20, 97

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")
