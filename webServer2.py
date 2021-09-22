# importing flask module
from flask import Flask, render_template, request, flash, redirect, url_for
from waitress import serve
import json
# follow error back to source
import traceback
import socket

class WebServer:
    def __init__(self,port=4433):
        self.__app = Flask(__name__)
        self.__port = port
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((testIP,0))
        self.__ip = s.getsockname()[0]
        self.__hostTest = socket.gethostname()
        serve(self.__app, host=self.__ip, port=self.__port)
    
    #getters to return webserver info
    def getIP(self):
        return self.__ip
    def getPort(self):
        return self.__port
    def getHost(self):
        return self.__hostTest
    
    # decorating index function with the app.route
        @app.route('/')
    def index(self):
        with open("settings.json", "r") as f:
            context = json.load(f)
            f.close()
            return render_template('/index.html', context=context)

    def index_error(self,error):
        with open("settings.json", "r") as f:
            context = json.load(f)
            f.close()
            return render_template('/index.html', context=context, error=error)

        @app.route('/settings', methods=['POST'])
    def update_settings(self):
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
    def server_connection_test(self):
        print("server connection tested\n")
        return render_template('server_connection_test.html')
            
