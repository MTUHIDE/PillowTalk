        from time import sleep
import itertools
import smbus

"""
ID 1 and 2 are for pillow 1 control, ID 1 for inflating and ID 2 for deflating
ID 3 and 4 are for pillow 2 control, ID 3 for inflating and ID 4 for Deflating
0x00 is off
0xFF is ON
"""


class MotorControl:
	# Initalize pin placements and set the pins to output
	# pin 1inflate pillow 1, pin 2 deflate pillow1, pin 3 inflate pillow 2, pin 4 deflate pillow 2
	def __init__(self):
		self._DEVICE_BUS = 1
		self._DEVICE_ADDR = 0x10
		self._bus = smbus.SMBus(self._DEVICE_BUS)

	def stopAll(self):
		self._bus.write_byte_data(self._DEVICE_ADDR, 1, 0x00)
		self._bus.write_byte_data(self._DEVICE_ADDR, 2, 0x00)
		self._bus.write_byte_data(self._DEVICE_ADDR, 3, 0x00)
		self._bus.write_byte_data(self._DEVICE_ADDR, 4, 0x00)

	def motor1On(self, time):
		return self.motorRun(time, 1)

	def motor2On(self, time):
		return self.motorRun(time, 2)

	def motor3On(self, time):
		return self.motorRun(time, 3)
	
	def motor4On(self, time):
		return self.motorRun(time, 4)

	def motor1Off(self, time):
		self._bus.write_byte_data(self._DEVICE_ADDR, 1, 0x00)

	def motor2Off(self, time):
		self._bus.write_byte_data(self._DEVICE_ADDR, 2, 0x00)
	
	def motor3Off(self, time):
		self._bus.write_byte_data(self._DEVICE_ADDR, 3, 0x00)
	
	def motor4Off(self, time):
		self._bus.write_byte_data(self._DEVICE_ADDR, 4, 0x00)

	def inflateAll(self, time):
		return self.motorRun2(time, 1, 3)

	def deflateAll(self, time):
		return self.motorRun2(time, 2, 4)
	
	def wait(self, time, motor, motor2 = None):
		for x in range(time):
			if motor2 != None:
				print("motor {} and motor {} on {} second".format(motor, motor2, x))
				if self._bus.read_byte_data(self._DEVICE_ADDR, motor) == 0 or self._bus.read_byte_data(self._DEVICE_ADDR, motor2) == 0:
                	return -2
			else:
				print("motor {} on {} second".format(motor, x))
				if self._bus.read_byte_data(self._DEVICE_ADDR, motor) == 0:
					return -2
			sleep(1)

	def checkDomain(self, motor, motor2 = None):
		if motor < 1 or motor > 4:
			return -1
		if motor2 != None:
			if ((motor == 1 and motor2 == 2) or (motor == 3 and motor2 == 4) or (motor2 == 2 and motor == 1) or (motor2 == 4 and motor2 == 3)) and (motor2 < 1 or motor2 > 4):
                return -1

		return 0
	
	# return -1 error in motor
	# return -2 Motor stopped early
	# Run the specified motor for a specified amount of time
	def motorRun(self, time, motor):
		checkDomain(motor)

		# Assuming pillow 1 is left and Pillow 2 is right
		if motor == 1:
			self._bus.write_byte_data(self._DEVICE_ADDR, 1, 0xFF)
			self._bus.write_byte_data(self._DEVICE_ADDR, 2, 0x00)
		if motor == 2:
			self._bus.write_byte_data(self._DEVICE_ADDR, 1, 0x00)
			self._bus.write_byte_data(self._DEVICE_ADDR, 2, 0xFF)
		if motor == 3:
			self._bus.write_byte_data(self._DEVICE_ADDR, 3, 0xFF)
			self._bus.write_byte_data(self._DEVICE_ADDR, 4, 0x00)
		if motor == 4:
			self._bus.write_byte_data(self._DEVICE_ADDR, 3, 0x00)
			self._bus.write_byte_data(self._DEVICE_ADDR, 4, 0xFF)
		
		self.wait(time, motor)

		if motor == 1 or motor == 2:
			self._bus.write_byte_data(self._DEVICE_ADDR, 1, 0x00)
			self._bus.write_byte_data(self._DEVICE_ADDR, 2, 0x00)
		if motor == 3 or motor == 4:
			self._bus.write_byte_data(self._DEVICE_ADDR, 3, 0x00)
			self._bus.write_byte_data(self._DEVICE_ADDR, 4, 0x00)

		print ("motor Finished")
		return 0
		
	#return -1 error in motor
	#return -2 Motor Stopped early
	def motorRun2(self, time, motor, motor2):
		checkDomain(motor, motor2)    

        # Assuming pillow 1 is left and Pillow 2 is right
        if motor == 1 or motor2 == 1:
            self._bus.write_byte_data(self._DEVICE_ADDR, 1, 0xFF)
            self._bus.write_byte_data(self._DEVICE_ADDR, 2, 0x00)
        if motor == 2 or motor2 == 2:
            self._bus.write_byte_data(self._DEVICE_ADDR, 1, 0x00)
            self._bus.write_byte_data(self._DEVICE_ADDR, 2, 0xFF)
        if motor == 3 or motor2 == 3:
            self._bus.write_byte_data(self._DEVICE_ADDR, 3, 0xFF)
            self._bus.write_byte_data(self._DEVICE_ADDR, 4, 0x00)
        if motor == 4 or motor2 == 4:
            self._bus.write_byte_data(self._DEVICE_ADDR, 3, 0x00)
            self._bus.write_byte_data(self._DEVICE_ADDR, 4, 0xFF)
                
		self.wait(time, motor, motor2)

        self.stopAll()

        print ("motor Finished")
        return 0

	# cycle everything based on given number of loops
	def cycleLoop(self, inflateTime, deflateTime, waitTime, loopNumber):
                totalTime = inflateTime + deflateTime + (waitTime*2-waitTime)
                totalLoopTime = totalTime*loopNumber
                print ("Starting cycle with estimated cycle total time of {}".format(self.timeFormat(totalLoopTime)))
                for i in range(loopNumber):
                        print("On Loop {}".format(i))
                        if self.motorRun2(inflateTime, 1, 3) == -2:
                                break;
                        for j in range(waitTime):
                                sleep(1)
                                print("wait {}".format(j))

                        if self.motorRun2(deflateTime, 2, 4) == -2:
                                break;
                        if i < loopNumber-1:
                                for j in range(waitTime):
                                        sleep(1)
                                        print("wait {}".format(j))

                return "Cycle Complete"

	# convert seconds given into hour,minute,sec
	def timeFormat(self, seconds):
		seconds = seconds % (24 * 3600)
		hour = seconds // 3600
		seconds %= 3600
		minutes = seconds // 60
		seconds %= 60
		return "%d:%02d:%02d" % (hour, minutes, seconds)
