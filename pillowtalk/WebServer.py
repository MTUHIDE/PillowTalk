from flask import Flask, make_response, render_template, request
from waitress import serve

from threading import Thread

# from MotorControl import *

from time import sleep

import json

app = Flask(__name__)

@app.route("/")
def index():
    '''
    Load webpage for user control
    '''
    context = None
    with open("settings.json", "r") as f:
        context = json.load(f)

    return render_template("index.html", context=context)


@app.route("/settings", methods=["POST"])
def settings():
    '''
    Send stuff here to update settings
    '''

    if request.method == 'POST':
        with open("settings.json", "w") as f:
            context = {}
            context["cushion_1_nickname"] = request.form["cushion_1_nickname"]
            context["cushion_2_nickname"] = request.form["cushion_2_nickname"]
            context["cushion_1_time"] = request.form["cushion_1_time"]
            context["cushion_2_time"] = request.form["cushion_2_time"]

            json.dump(context, f)

        return make_response()


@app.route("/motorcontrol", methods=["POST"])
def motorcontrol():
    '''
    Accepts a POST request and controls motors
    TODO: Describe this better

    Request should look like the following:
    {
        "motors" : [
            {"motor": 1, "time": 30},
            {"motor": 2, "time": 20}
        ]
    }
    '''
    mc = MotorControl()
    body = {}
    if request.method == "POST":
        body = request.get_json()

        # TODO: Connect this to the motor controller

        return body


@app.route("/parse")
def textparsing():
    '''
    Accepts a POST request and sends data to the text parser
    TODO: Describe this better

    Request should look like the following:
    {
        "text": "this is some text that I'd like to parse"
    }
    '''

    body = {}
    if request.method == "POST":
        body = request.get_json()
        # TODO: Connect this to text parser
        return body


@app.route("/healthcheck")
def healthcheck():
    '''
    Health check to make sure the server is at least sort of working correctly
    '''
    return "OK"


@app.route("/threadtest")
def threadtest():
    '''
    Test endpoint to demonstrate creating a thread, sleeping, and then exiting while allowing Flask to respond quickly
    '''
    class TestThread(Thread):
        def __init__(self):
            super().__init__()

        def run(self):
            print("Starting")
            sleep(5)
            print(f"Done)")

    temp = TestThread()
    temp.start()

    return make_response()


# Start the app on localhost:3000
app.run("0.0.0.0", 3000)
# serve(app)
