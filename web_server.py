# requires python2.7
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

# one concurrent command flag
is_running1 = False
is_running2 = False
relay = RelayControl()
# decorating index function with the app.route
@app.route('/')
def index():
    with open("settings.json", "r") as f:
        context = json.load(f)
        f.close()
        return render_template('/index.html', context=context)

def index_error(error):
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

### Lists of commands ###
# inflate name x : inflates an 'x' amount of seconds on motor name
# deflate name x : deflates an 'x' amount of seconds on motor name
@app.route('/command', methods=['POST'])
def command():
	if request.method == 'POST':
                max_seconds = 10
		global is_running1
		global is_running2
		global relay
                command_form = request.form['command']
		# print command
                split = command_form.split()

                #if is_running:
                #    return index_error("Already running a command")

                if len(split) < 3 or not split[2].isnumeric():
                    return index_error("Inproper syntax")

                command = split[0]
		relayName = split[1]
                waitTime = int(split[2])

		# Check to see if the specified cushion is in use
		if relayName == "cushion_1" and is_running1:
		    return index_error("Already running that command")
		    print "already running cushion1"
		elif relayName == "cushion_2" and is_running2:
                    return index_error("already running that command")
		    print "already running cushion2"

		# Check to see if the specified time requested for the relay is not out of bounds
		if waitTime > max_seconds or waitTime < 0:
                    return index_error("Duration too long")

                try:
		    # Call run relay for the specified cushion and set that cushion to be running
                    if command == "inflate":
			if relayName == "cushion_1":
			    is_running1 = True
			    relay.relayRun(waitTime, 1)
			elif relayName == "cushion_2":
			    is_running2 = True
			    relay.relayRun(waitTime, 2)
			else:
			    return index_error("invalid command")
                        print "inflating " + motorName + " for " + str(waitTime) + " seconds"
		    # Call run relay for the specified cushion and set that cushion to be running 
                    elif command == "deflate":
                        if relayName == "cushion_1":
			    is_running1 = True
			    relay.relayRun(waitTime, 3)
			    print "deflating"
			elif relayName == "cushion_2":
			    is_running2 = True
			    relay.relayRun(WaitTime, 4)
			    print "deflating"
			else:
			    return index_error("invalid command")

                        print "deflating " + motorName + " for " + str(waitTime) + " seconds"

                    else:
                        return index_error("Invalid command")
		# Keyboard interrupt exception handler
                except KeyboardInterrupt:
                    print "\nWhy did keyboard stop program\n"
		    relay.exit()
		# Other interrupt exception handler
                except Exception:
                    print "\nWhy did something else stop program\n"
                    traceback.print_exc()

                finally:
		    # set the specified cushion to not be running
		    if relayName == "cushion_1":
		        is_running1 = False
		    elif relayName == "cushion_2":
			is_running2 = False
		    else:
			return index_error("invalid command")

                #is_running = False
                return index()


if __name__ == "__main__":
	# Find the local ip of the raspberry pi to run the flask server off of
	testIP = "8.8.8.8"
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect((testIP,0))
	ip = s.getsockname()[0]
	hostTest = socket.gethostname()
	print "IP: " + ip + " HOST: " + hostTest

	host = ip
	port = "4433"
	serve(app, host=host, port=port)
