#requires python2.7
# importing flask module
from flask import Flask, render_template, request
from waitress import serve

# initializing a variable of Flask
app = Flask(__name__)

# decorating index function with the app.route
@app.route('/')
def index():
   return render_template('/index.html')

### Lists of commands ###
# inflate x : inflates an 'x' amount of seconds
# deflate x : deflates an 'x' amount of seconds
@app.route('/command', methods=['POST'])
def command():
	if request.method == 'POST':
		command = request.form['command']
		# print command
                split = command.split()
                if split[0] == "inflate":
                    print "inflating " + split[1]
                elif split[0] == "deflate":
                    print "deflating " + split[1]

		return render_template('/index.html')


if __name__ == "__main__":
	host = "192.168.1.27"
	port = "4433"
	serve(app, host=host, port=port)
