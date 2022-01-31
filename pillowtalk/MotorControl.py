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
    # return -1 error in relay
    # return -2 Motor stopped early
    # Run the specified relay for a specified amount of time

    def relayRun(self, time, relay):
        if relay <= 0 or relay > 4:
            return -1
        # Assuming pillow 1 is left and Pillow 2 is right
        if relay == 1:
            self._bus.write_byte_data(self._DEVICE_ADDR, 1, 0xFF)
            self._bus.write_byte_data(self._DEVICE_ADDR, 2, 0x00)
        if relay == 2:
            self._bus.write_byte_data(self._DEVICE_ADDR, 1, 0x00)
            self._bus.write_byte_data(self._DEVICE_ADDR, 2, 0xFF)
        if relay == 3:
            self._bus.write_byte_data(self._DEVICE_ADDR, 3, 0xFF)
            self._bus.write_byte_data(self._DEVICE_ADDR, 4, 0x00)
        if relay == 4:
            self._bus.write_byte_data(self._DEVICE_ADDR, 3, 0x00)
            self._bus.write_byte_data(self._DEVICE_ADDR, 4, 0xFF)
        for x in range(time):
            if self._bus.read_byte_data(self._DEVICE_ADDR, relay) == 0:
                return -2
            #print("{}: {}".format(relay, self._bus.read_byte_data(self._DEVICE_ADDR, relay)))
            sleep(1)
            print("Relay {} on {} second".format(relay, x))

        if relay == 1 or relay == 2:
            self._bus.write_byte_data(self._DEVICE_ADDR, 1, 0x00)
            self._bus.write_byte_data(self._DEVICE_ADDR, 2, 0x00)
        if relay == 3 or relay == 4:
            self._bus.write_byte_data(self._DEVICE_ADDR, 3, 0x00)
            self._bus.write_byte_data(self._DEVICE_ADDR, 4, 0x00)

        print("Relay Finished")
        return 0
    # return -1 error in relay
    # return -2 Motor Stopped early

    def relayRun2(self, time, relay, relay2):
        if (relay == 1 and relay2 == 2) or (relay == 3 and relay2 == 4) or (relay2 == 1 and relay == 1) or (relay2 == 3 and relay2 == 4):
            return -1
        if relay <= 0 or relay > 4 or relay2 <= 0 or relay2 > 4:
            return -1
        # Assuming pillow 1 is left and Pillow 2 is right
        if relay == 1 or relay2 == 1:
            self._bus.write_byte_data(self._DEVICE_ADDR, 1, 0xFF)
            self._bus.write_byte_data(self._DEVICE_ADDR, 2, 0x00)
        if relay == 2 or relay2 == 2:
            self._bus.write_byte_data(self._DEVICE_ADDR, 1, 0x00)
            self._bus.write_byte_data(self._DEVICE_ADDR, 2, 0xFF)
        if relay == 3 or relay2 == 3:
            self._bus.write_byte_data(self._DEVICE_ADDR, 3, 0xFF)
            self._bus.write_byte_data(self._DEVICE_ADDR, 4, 0x00)
        if relay == 4 or relay2 == 4:
            self._bus.write_byte_data(self._DEVICE_ADDR, 3, 0x00)
            self._bus.write_byte_data(self._DEVICE_ADDR, 4, 0xFF)
        for x in range(time):
            if self._bus.read_byte_data(self._DEVICE_ADDR, relay) == 0 or self._bus.read_byte_data(self._DEVICE_ADDR, relay2) == 0:
                return -2
            sleep(1)
            print("Relay {},{} on {} second".format(relay, relay2, x))

        if relay == 1 or relay == 2 or relay2 == 1 or relay2 == 2:
            self._bus.write_byte_data(self._DEVICE_ADDR, 1, 0x00)
            self._bus.write_byte_data(self._DEVICE_ADDR, 2, 0x00)
        if relay == 3 or relay == 4 or relay2 == 3 or relay2 == 4:
            self._bus.write_byte_data(self._DEVICE_ADDR, 3, 0x00)
            self._bus.write_byte_data(self._DEVICE_ADDR, 4, 0x00)

        print("Relay Finished")
        return 0

    # cycle everything based on given number of loops
    def cycleLoop(self, inputTime, outputTime, waitTime, loopNumber):
        totalTime = inputTime + outputTime + (waitTime*2-waitTime)
        totalLoopTime = totalTime*loopNumber
        print("Starting cycle with estimated cycle total time of {}".format(
            self.timeFormat(totalLoopTime)))
        for i in range(loopNumber):
            print("On Loop {}".format(i))
            if self.relayRun2(inputTime, 1, 3) == -2:
                break
            for j in range(waitTime):
                sleep(1)
                print("wait {}".format(j))

            if self.relayRun2(outputTime, 2, 4) == -2:
                break
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
