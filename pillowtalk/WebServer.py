from flask import Flask, make_response, render_template, request
import json
from MotorControl import *
from TextParser import TextParser
from threading import Thread
from time import sleep
from waitress import serve


app = Flask(__name__)

tp = TextParser()


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

    body = {}
    if request.method == "POST":
        body = request.get_json()
        seen = set()
        try:
            for command in body["motors"]:
                currMotor: int = command["motor"]
                currTime: int = command["time"]
                # Check if motor n is even and make sure n - 1 has not been used yet
                # Also do the same for odd numbers and n + 1
                if (not ((currMotor % 2 == 0 and currMotor - 1 in seen) or (currMotor % 2 == 1 and currMotor + 1 in seen))) and currMotor not in seen:
                    try:
                        print(f"Running motor {currMotor} for {currTime}")
                        seen.add(currMotor)
                        runMotor(currMotor, currTime)
                    except:
                        print(f"Skipping motor {currMotor}")

        except Exception as e:
            return e, 400

        return "Success", 200


@app.route("/parse", methods=["POST"])
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
        try:
            body = request.get_json()
            print(body["text"])
            tp.runCommands(body["text"])
        except Exception as e:
            print(e)

    return "Success", 200


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
