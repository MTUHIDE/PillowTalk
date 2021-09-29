import RPi.GPIO as GPIO
from time import sleep
import itertools
import smbus
GPIO.setwarnings(False)

"""
For the relay control of the motor, the RPI.GPIO may be uneeded.
"""

"""
ID 1 and 2 are for pillow 1 control, ID 1 for inflating and ID 2 for deflating
ID 3 and 4 are for pillow 2 control, ID 3 for inflating and ID 4 for Deflating
0x00 is off
0xFF is ON
"""
class RelayControl:
	# Initalize pin placements and set the pins to output
	#pin 1inflate pillow 1, pin 2 deflate pillow1, pin 3 inflate pillow 2, pin 4 deflate pillow 2
	def __init__(self):
    
	DEVICE_BUS = 1
	DEVIVE_ADDR = 0x10
	bus = smbus.SMBus(DEVICE_BUS)

	# Run the specified relay for a specified amount of time
	def relayRun(self, time, relay):
		# Assuming pillow 1 is left and Pillow 2 is right
		if relay == 1:
			bus.write_byte_data(DEVICE_ADDR, 1, 0xFF)
			bus.write_byte_data(DEVICE_ADDR, 2, 0x00)
			# Make sure that right pillow is off
			bus.write_byte_data(DEVICE_ADDR, 3, 0x00)
			bus.write_byte_data(DEVICE_ADDR, 4, 0x00)
		elif relay == 2:
			bus.write_byte_data(DEVICE_ADDR, 1, 0x00)
			bus.write_byte_data(DEVICE_ADDR, 2, 0xFF)
			# Make sure that right pillow is off
			bus.write_byte_data(DEVICE_ADDR, 3, 0x00)
			bus.write_byte_data(DEVICE_ADDR, 4, 0x00)
		elif relay == 3:
			# Make sure that left pillow is off
			bus.write_byte_data(DEVICE_ADDR, 1, 0x00)
			bus.write_byte_data(DEVICE_ADDR, 2, 0x00)

			bus.write_byte_data(DEVICE_ADDR, 3, 0xFF)
			bus.write_byte_data(DEVICE_ADDR, 4, 0x00)
		elif relay == 4:
			# Make sure left pillow is off
			bus.write_byte_data(DEVICE_ADDR, 1, 0x00)
			bus.write_byte_data(DEVICE_ADDR, 2, 0x00)

			bus.write_byte_data(DEVICE_ADDR, 3, 0x00)
			bus.write_byte_data(DEVICE_ADDR, 4, 0xFF)

		for x in range(time):
			sleep(1)
			print "Relay " + str(relay) + " " + str(x)

		print "Relay Finished"

	#cycle everything based on given number of loops
	# def cycleLoop(self, InputTime, outputTime, waitTime, loopNumber):
	# 	totalTime = InputTime + outputTime + waitTime
	# 	print "Starting cycle with estimated cycle total time of " + convertSecs(loopNumber * totalTime)
	# 	for x in range(loopNumber):
	# 		GPIO.output(self.pin1, True)
	# 		GPIO.output(self.pin3, True)
	# 		sleep(cushionTime)
	# 		GPIO.output(self.pin1, False)
	# 		GPIO.output(self.pin3, False)
	# 		sleep(waitTime)
	# 		GPIO.output(self.pin2, True)
	# 		GPIO.output(self.pin4, True)
	# 		sleep(cushionTime-1)
	# 		GPIO.output(self.pin2, False)
	# 		GPIO.output(self.pin4, False)
	# 	print "Cycle Complete"
		
	#cycle everything based on given number of hours
            #def cycleTime(self, InputTime, outputTime, waitTime, totalHours):
            #	totalTime = InputTime + outputTime + waitTime
	#cycle each individual pillow based on given number of hours
	#def inflateMultiPillow(self, timeInput, timeOutput, timeWait, totalHours):
	#	if (len(timeInput) != len(timeOutput) or len(timeInput) != len(timeWait)):
	#		return error
     # 		seconds = convertHours(totalHours)
      #		totalLoops = []
      #		for (i, o, w) in zip(timeInput, timeOutput, timeWait)
       # 		t = i + o + w
        #  		totalLoops.append(seconds/t)
#Finish here!!!

	#convert seconds given into hour,minute,sec

	def convertSecs(seconds):
		seconds = seconds % (24 *3600)
		hour = second // 3600
		seconds %= 3600
		minutes = seconds // 60
		seconds %= 60
		return  "%d:%02d:%02d" % (hour, minutes, seconds)

	# convert hours to seconds
	def convertHours(hours):
		return hours*60*60

	# Reset the pins mode and clean up any changed settings on the pins
	# def exit(self):
	# 	GPIO.cleanup()
