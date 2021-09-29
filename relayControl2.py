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
		elif relay == 2:
			bus.write_byte_data(DEVICE_ADDR, 1, 0x00)
			bus.write_byte_data(DEVICE_ADDR, 2, 0xFF)
		elif relay == 3:
			bus.write_byte_data(DEVICE_ADDR, 3, 0xFF)
			bus.write_byte_data(DEVICE_ADDR, 4, 0x00)
		elif relay == 4:
			bus.write_byte_data(DEVICE_ADDR, 3, 0x00)
			bus.write_byte_data(DEVICE_ADDR, 4, 0xFF)

		for x in range(time):
			sleep(1)
			print "Relay " + str(relay) + " " + str(x)

		print "Relay Finished"

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
