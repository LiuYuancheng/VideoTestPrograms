#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        attackHost.py [python2.7/python3]
#
# Purpose:     This program is just a sample flask web server. 
# Created:     2021/03/08
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------
import socket
import requests
import math
import time
from flask import Flask, redirect, url_for, request, render_template

TEST_MODE = True # Test mode flag - True: test on local computer

# Init the flask web server program.
app = Flask(__name__)


@app.route('/')
def index():
    # Add CSS in the html for flask is shown in this link: 
    # https://pythonhow.com/add-css-to-flask-website/
    return render_template('index.html')
    #return render_template('index.html.jinja')


if __name__ == '__main__':
    app.run(host= "0.0.0.0", debug=False, threaded=True)
   