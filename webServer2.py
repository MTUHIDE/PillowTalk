# importing flask module
from flask import Flask, render_template, request, flash, redirect, url_for
from waitress import serve
import json
# follow error back to source
import traceback
import socket
# implementation of motorControl Class
from relayControl import *

# initializing a variable of Flask
app = Flask(__name__)

# text parser and motor control classes
from MotorControl import *
from TextParser import *
text = TextParser()

# decorating index function with the app.route
@app.route('/')
def index():
    with open("settings.json", "r") as f:
        context = json.load(f)
        f.close()
        return render_template('/index.html', context=context)


def index_error(error):
    print(error)
    with open("settings.json", "r") as f:
        context = json.load(f)
        f.close()
        return render_template('/index.html', context=context, error=error)


@app.route('/settings', methods=['POST'])
def update_settings():
    if request.method == 'POST':
        with open("settings.json", "r+") as f:
            context = json.load(f)
            context['cushion_1_nickname'] = request.form['cushion_1_nickname']
            context['cushion_2_nickname'] = request.form['cushion_2_nickname']
            context['cushion_1_time'] = request.form['cushion_1_time']
            context['cushion_2_time'] = request.form['cushion_2_time']
            f.truncate(0)
            f.seek(0)
            json.dump(context, f)
            f.close()
            return redirect(url_for('index'))


@app.route('/server_connection_test', methods=['GET'])
def server_connection_test():
    print("server connection tested\n")
    return render_template('server_connection_test.html')

@app.route('/command', methods=['POST'])
def command():
    if request.method == 'POST':
      #submit command for error checking and return relay
        command_form = request.form['command']
        print(command_form)
        command = text.commandSearch(command_form)
        print(command)
        if command == -2:
            return index_error("Command incomplete")
        relay = text.returnRelay(command)
        print(relay)
        if relay == -1:
            return index_error("Invalid Number")
        elif relay == -2:
            return index_error("Invalid Action")
        elif relay == -3:
            return index_error("Invalid Inflatable")

    #motor function

    return index()

if __name__ == "__main__":
    # Find the local ip of the raspberry pi to run the flask server off of
    testIP = "8.8.8.8"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((testIP, 0))
    ip = s.getsockname()[0]
    hostTest = socket.gethostname()
    # send back to main ip host test
    print("IP: " + ip + " HOST: " + hostTest)
    port = "4433"
    serve(app, host=ip, port=port)
