import RPi.GPIO as GPIO
from time import sleep

class MotorControl:
	def __init__(self):
		self.in1 = 11
		self.in2 = 13
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.in1, GPIO.OUT)
		GPIO.setup(self.in2, GPIO.OUT)


	def motorOn(self, time):
		GPIO.output(self.in1, True)
		#GPIO.output(self.in2, True)

		for x in range(time):
			sleep(1)
			print ("sleep for {}".format(x))

		GPIO.output(self.in1, False)
		#GPIO.output(self.in2, False)
