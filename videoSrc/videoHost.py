#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        attackHost.py [python2.7/python3]
#
# Purpose:     This program is just a sample flask web server. 
# Created:     2021/03/08
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------
import os, sys
import socket
import requests
import math
import time
from flask import Flask, redirect, url_for, request, render_template
from flask_socketio import SocketIO, emit


TEST_MODE = True # Test mode flag - True: test on local computer
thread = None

# Init the flask web server program.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG'] = True  
iSocketIO = SocketIO(app)

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        iSocketIO.sleep(10)
        count += 1
        iSocketIO.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')

@app.route('/')
def index():
    # Add CSS in the html for flask is shown in this link: 
    # https://pythonhow.com/add-css-to-flask-website/
    return render_template('index_video.html')
    #return render_template('index.html.jinja')

@iSocketIO.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})

@iSocketIO.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')

@iSocketIO.on('connect', namespace='/test')
def test_connect():
    global thread
    if thread is None:
        thread = iSocketIO.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})

@iSocketIO.on('disconnect')
def test_disconnect():
    print('Client disconnected')

#----------------------------------------------------------------------------------------------------
def main():
    # Init the logger: 
    TOPDIR = 'src'                      # folder name where we put Logs, Maps, etc
    gWD = os.getcwd()
    idx = gWD.find(TOPDIR)
    if idx != -1:
        gTopDir = gWD[:idx + len(TOPDIR)]
    else:
        gTopDir = gWD   # did not find TOPDIR - use WD
    print('gTopDir:%s' % gTopDir)
    iSocketIO.run(app, host="0.0.0.0", port=5000)

if __name__ == '__main__':
    main()
    print('End of __main__')