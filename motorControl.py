import RPi.GPIO as GPIO
from time import sleep

class MotorControl:
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		self.in1 = 11
		self.in2 = 13
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.in1, GPIO.OUT)
		GPIO.setup(self.in2, GPIO.OUT)

	def motorOn(self, time, motorNumber):
		if motorNumber == 1:
			GPIO.output(self.in1, True)
		elif motorNumber == 2:
			GPIO.output(self.in2, True)
		for x in range(time):
			sleep(1)
			print "Motor " + str(motorNumber) + " " + str(x)

		if motorNumber == 1:
			GPIO.output(self.in1, False)
		elif motorNumber == 2:
			GPIO.output(self.in2, False)
		GPIO.output(self.in1, False)
		print "Motor Finished"

	def exit(self):
		GPIO.cleanup()
