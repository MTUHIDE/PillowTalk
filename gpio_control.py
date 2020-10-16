from flask import Flask
from flask_ask import Ask, statement, convert_errors
import RPi.GPIO as GPIO
import logging

GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
ask = Ask(app, '/')

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.intent('GPIOControlIntent', mapping={'status': 'status'})
def gpio_status(status):

    if status in ['on','high' ]:
      GPIO.setup(21, GPIO.IN)
      state = GPIO.input(21)
      if (state == True):
        GPIO.setup(21, GPIO.OUT)
        GPIO.output(21,GPIO.HIGH)
        return statement('Lights are already on')
      else:
        GPIO.setup(21, GPIO.OUT)
        GPIO.output(21,GPIO.HIGH)
        return statement('Turning lights {}'.format(status))

    if status in ['off','low' ]:
      GPIO.setup(21, GPIO.IN)
      state = GPIO.input(21)
      print('status of light',state)
      if (state == False):
        GPIO.setup(21, GPIO.OUT)
        GPIO.output(21,GPIO.LOW)
        return statement('Lights are already off')
      else:
        GPIO.setup(21, GPIO.OUT)
        GPIO.output(21,GPIO.LOW)
        return statement('Turning lights {}'.format(status))

if __name__ == '__main__':
  port = 5000 #the custom port you want
  app.run(host='0.0.0.0', port=port)
