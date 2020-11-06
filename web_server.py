# requires python2.7
# importing flask module
from flask import Flask, render_template, request, flash
from waitress import serve
# follow error back to source
import traceback

# implementation of motorControl Class
from motorControl import *

# initializing a variable of Flask
app = Flask(__name__)

# one concurrent command flag
is_running1 = False
is_running2 = False
motor = MotorControl()
# decorating index function with the app.route
@app.route('/')
def index():
    return render_template('/index.html')

def index_error(error):
    return render_template('/index.html', error=error)

### Lists of commands ###
# inflate name x : inflates an 'x' amount of seconds on motor name
# deflate name x : deflates an 'x' amount of seconds on motor name
@app.route('/command', methods=['POST'])
def command():
	if request.method == 'POST':
                max_seconds = 10
		global is_running1
		global is_running2
		global motor
                command_form = request.form['command']
		# print command
                split = command_form.split()

                #if is_running:
                #    return index_error("Already running a command")

                if len(split) < 3 or not split[2].isnumeric():
                    return index_error("Inproper syntax")

                command = split[0]
		motorName = split[1]
                waitTime = int(split[2])

		if motorName == "cushion_1" and is_running1:
		    return index_error("Already running that command")
		    print "already running cushion1"
		elif motorName == "cushion_2" and is_running2:
                    return index_error("already running that command")
		    print "already running cushion2"

		if waitTime > max_seconds:
                    return index_error("Duration too long")

                try:
                    if command == "inflate":
			if motorName == "cushion_1":
			    is_running1 = True
			    motor.motorOn(waitTime, 1)
			elif motorName == "cushion_2":
			    is_running2 = True
			    motor.motorOn(waitTime, 2)
			else:
			    return index_error("invalid command")
                        print "inflating " + motorName + " for " + str(waitTime) + " seconds"

                    elif command == "deflate":
                        if motorName == "cushion_1":
			    print "deflating"
			elif motorName == "cushion_2":
			    print "deflating"
			else:
			    return index_error("invalid command")

                        print "deflating " + motorName + " for " + str(waitTime) + " seconds"

                    else:
                        # flash("hiiii")
                        return index_error("Invalid command")

                except KeyboardInterrupt:
                    print "\nWhy did keyboard stop program\n"
		    motor.exit()

                except Exception:
                    print "\nWhy did something else stop program\n"
                    traceback.print_exc()

                finally:
		    if motorName == "cushion_1":
		        is_running1 = False
		    elif motorName == "cushion_2":
			is_running2 = False
		    else:
			return index_error("invalid command")

                #is_running = False
                return index()


if __name__ == "__main__":
	host = "192.168.1.27"
	port = "4433"
	serve(app, host=host, port=port)
