import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)

class RelayControl:
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		self.in1 = 11
		self.in2 = 13
		self.in3 = 15
		self.in4 = 16
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.in1, GPIO.OUT)
		GPIO.setup(self.in2, GPIO.OUT)

	def relayRun(self, time, relay):
		if relay == 1:
			GPIO.output(self.in1, True)
		elif relay == 2:
			GPIO.output(self.in2, True)
		elif relay == 3:
			GPIO.output(self.in3, True)
		elif relay == 4:
			GPIO.output(self.in4, True)

		for x in range(time):
			sleep(1)
			print "Relay " + str(relay) + " " + str(x)

		if relay == 1:
			GPIO.output(self.in1, False)
		elif relay == 2:
			GPIO.output(self.in2, False)
		elif relay == 3:
			GPIO.output(self.in3, False)
		elif relay == 4:
			GPIO.output(self.in4, False)
		print "Relay Finished"

	def exit(self):
		GPIO.cleanup()
