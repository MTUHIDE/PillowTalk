import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)

class RelayControl:
	# Initalize pin placements and set the pins to output
	#pin 1inflate pillow 1, pin 2 deflate pillow1, pin 3 inflate pillow 2, pin 4 deflate pillow 2
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
			pin = self.pin1
		elif relay == 2:
			GPIO.output(self.pin2, True)
			pin = self.pin2
		elif relay == 3:
			GPIO.output(self.pin3, True)
			pin = self.pin3
		elif relay == 4:
			GPIO.output(self.pin4, True)
			pin = self.pin4

		for x in range(time):
			sleep(1)
			print "Relay " + str(pin) + " " + str(x)

		if relay == 1:
			GPIO.output(self.pin1, False)
		elif relay == 2:
			GPIO.output(self.pin2, False)
		elif relay == 3:
			GPIO.output(self.pin3, False)
		elif relay == 4:
			GPIO.output(self.pin4, False)
		print "Relay Finished"

	#cycle everything based on time given
	def cycle(self, cushionTime, waitTime, loopNumber):
		totalTime = (cushionTime * 2) + waitTime
		print "Starting cycle with estimated cycle total time of " + convert(loopNumber * cushionTime)
		for x in range(loopNumber):
			GPIO.output(self.pin1, True)
			GPIO.output(self.pin3, True)
			sleep(cushionTime)
			GPIO.output(self.pin1, False)
			GPIO.output(self.pin3, False)
			sleep(waitTime)
			GPIO.output(self.pin2, True)
			GPIO.output(self.pin4, True)
			sleep(cushionTime-1)
			GPIO.output(self.pin2, False)
			GPIO.output(self.pin4, False)
		print "Cycle Complete"

	#convert seconds given into hour,minute,sec
	def convert(seconds):
		seconds = seconds % (24 *3600)
		hour = second // 3600
		seconds %= 3600
		minutes = seconds // 60
		seconds %= 60
		return  "%d:%02d:%02d" % (hour, minutes, seconds)

	# Reset the pins mode and clean up any changed settings on the pins
	def exit(self):
		GPIO.cleanup()
