from flask import Flask, make_response, render_template
from waitress import serve

from threading import Thread

from time import sleep

import json

app = Flask(__name__)


@app.route("/")
def index():
    '''
    <Insert a really descriptive comment here>
    '''
    context = None
    with open("settings.json", "r") as f:
        context = json.load(f)

    return render_template("index.html", context=context)


@app.route("/settings")
def settings():
    '''
    Send stuff here to update settings
    '''
    pass


@app.route("/motorcontrol")
def motorcontrol():
    '''
    Send stuff here to control motors
    TODO: Figure out what input this should accept
    '''
    pass


@app.route("/parse")
def textparsing():
    '''
    Send text here to get parsed
    TODO: Figure out what input this should accept
    '''
    pass


@app.route("/healthcheck")
def healthcheck():
    '''
    Health check to make sure the server is at least sort of working correctly
    '''
    return "OK"


@app.route("/threadtest")
def threadtest():

    class TestThread(Thread):
        def __init__(self):
            super().__init__()

        def run(self):
            print("Starting")
            sleep(5)
            print("Done")

    temp = TestThread()
    temp.start()

    return make_response()


# Start the app on localhost:3000
app.run("0.0.0.0", 3000)
# serve(app)
