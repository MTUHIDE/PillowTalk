import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

class MotorControl:
	def __init__(self):
		self.motorControl = 11

	def mControl(self, command, time):
		try:
			time.sleep(time)

			GPIO.setup(motorgpio, GPIO.OUT)
			GPIO.output(motorgpio, GPIO.HIGH)

			for x in range(sleepTime):
				time.sleep(1)
				print (x)

			GPIO.output(motorgpio, GPIO.LOW)

		except KeyboardInterrupt:
			print ("\nwhy did you stop it\n")

		except:
			print ("\nwhy did something else stop it\n")

		finally:
			GPIO.cleanup()
