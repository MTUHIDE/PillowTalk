import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)

class RelayControl:
	# Initalize pin placements and set the pins to output
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		self.pin1 = 11
		self.pin2 = 13
		self.pin3 = 15
		self.pin4 = 16
		GPIO.setup(self.pin1, GPIO.OUT)
		GPIO.setup(self.pin2, GPIO.OUT)
		GPIO.setup(self.pin3, GPIO.OUT)
		GPIO.setup(self.pin4, GPIO.OUT)

	# Run the specified relay for a specified amount of time
	def relayRun(self, time, relay):
		if relay == 1:
			GPIO.output(self.pin1, True)
		elif relay == 2:
			GPIO.output(self.pin2, True)
		elif relay == 3:
			GPIO.output(self.pin3, True)
		elif relay == 4:
			GPIO.output(self.pin4, True)

		for x in range(time):
			sleep(1)
			print "Relay " + str(relay) + " " + str(x)

		if relay == 1:
			GPIO.output(self.pin1, False)
		elif relay == 2:
			GPIO.output(self.pin2, False)
		elif relay == 3:
			GPIO.output(self.pin3, False)
		elif relay == 4:
			GPIO.output(self.pin4, False)
		print "Relay Finished"

	# Reset the pins mode and clean up any changed settings on the pins
	def exit(self):
		GPIO.cleanup()
