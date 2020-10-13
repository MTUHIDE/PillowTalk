import RPi.GPIO as GPIO
import time

motorgpio = 11
sleepTime = 10

GPIO.setmode(GPIO.BOARD)

try:
	time.sleep(5)
	
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
