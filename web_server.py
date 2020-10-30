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
is_running = False

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
		global is_running
                max_seconds = 10

                command_form = request.form['command']
		# print command
                split = command_form.split()

                if is_running:
                    return index_error("Already running a command")

                if len(split) < 3 or not split[2].isnumeric():
                    return index_error("Inproper syntax")

                command = split[0]
		motorName = split[1]
                time = int(split[2])

                if time > max_seconds:
                    return index_error("Duration too long")

                try:
                    #initialize motorControl Class
                    motor = MotorControl()
                    # Command to perform
                    if command == "inflate":
			if motorName == "cushion_1":
				motor.motorOn(time, 1)
			elif motorName == "cushion_2":
				motor.motorOn(time, 2)
			else:
				return index_error("invalid command")
                        is_running = True
                        print "inflating " + motorName + " for " + str(time) + " seconds"
                    elif command == "deflate":
                        if motorName == "cushion_1":
				print ""
			elif motorName == "cushion_2":
				print ""
			else:
				return index_error("invalid command")
			is_running = True
                        print "deflating " + motorName + " for " + str(time) + " seconds"
                    else:
                        # flash("hiiii")
                        return index_error("Invalid command")

                except KeyboardInterrupt:
                    print "\nWhy did keyboard stop program\n"

                except Exception:
                    print "\nWhy did something else stop program\n"
                    traceback.print_exc()

                finally:
		    motor.exit()
		    print "Command finished"

                is_running = False
                return index()


if __name__ == "__main__":
	host = "192.168.1.27"
	port = "4433"
	serve(app, host=host, port=port)
