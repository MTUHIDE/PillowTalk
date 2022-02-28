from time import sleep
from enum import Enum

from threading import Thread, Lock

import itertools
import smbus

"""
ID 1 and 2 are for pillow 1 control, ID 1 for inflating and ID 2 for deflating
ID 3 and 4 are for pillow 2 control, ID 3 for inflating and ID 4 for Deflating
0x00 is off
0xFF is ON
"""

DEVICE_BUS = 1
DEVICE_ADDR = 0x10

bus = smbus.SMBus(DEVICE_BUS)

motorThreads = {}

class MotorThread(Thread):
    class MotorState(Enum):
        RUNNING = 0
        DONE = 1
    
    
    def __init__(self, motor: int, timeout: int):
        super().__init__()
        self.motor = motor
        self.timeout = timeout
        self.running = True

    def run(self):
        global bus

        print(f"Motor {self.motor} starting")
        while (self.timeout > 0 and self.running):
            if bus.read_byte_data(DEVICE_ADDR, self.motor) == 0:
                print(f"Motor {self.motor} stopped early for some reason")
                break
            sleep(1)

        if self.running:
            # Stop motor
            pass

    def updateTimeout(self, timeout):
        print(f"Set motor {self.motor}'s thread timeout to {timeout}")
        self.timeout = timeout

def stopAll():
    """
    Stop all motors
    """
    bus.write_byte_data(DEVICE_ADDR, 1, 0x00)
    bus.write_byte_data(DEVICE_ADDR, 2, 0x00)
    bus.write_byte_data(DEVICE_ADDR, 3, 0x00)
    bus.write_byte_data(DEVICE_ADDR, 4, 0x00)


def motor1On(time):
    motorRun(time, 1)


def motor2On(time):
    motorRun(time, 2)


def motor3On(time):
    motorRun(time, 3)


def motor4On(time):
    motorRun(time, 4)


def motor1Off(time):
    bus.write_byte_data(DEVICE_ADDR, 1, 0x00)


def motor2Off(time):
    bus.write_byte_data(DEVICE_ADDR, 2, 0x00)


def motor3Off(time):
    bus.write_byte_data(DEVICE_ADDR, 3, 0x00)


def motor4Off(time):
    bus.write_byte_data(DEVICE_ADDR, 4, 0x00)


def inflateAll(time):
    motorRun2(time, 1, 3)


def deflateAll(time):
    motorRun2(time, 2, 4)


def wait(time, motor, motor2=None):
    '''Given a list of motors, wait a specified time and check if they got turned off by something else'''
    for x in range(time):
        if motor2 != None:
            print(f"Motor {motor} and motor {motor2} on for {x} second(s)".format(
                motor, motor2, x))
            if bus.read_byte_data(DEVICE_ADDR, motor) == 0 or bus.read_byte_data(DEVICE_ADDR, motor2) == 0:
                raise MotorStoppedEarlyError("Motor Stopped Early Error")
        else:
            print(f"Motor {motor} on for {x} second(s)")
            if bus.read_byte_data(DEVICE_ADDR, motor) == 0:
                raise MotorStoppedEarlyError("Motor Stopped Early Error")
        sleep(1)


def checkDomain(motor, motor2=None):
    '''Check the validity of one or two motors being called'''
    if motor < 1 or motor > 4:
        raise InternalMotorError(f"{motor} is outside domain")
    if motor2 != None:
        if ((motor == 1 and motor2 == 2) or (motor == 3 and motor2 == 4) or (motor2 == 2 and motor == 1) or (motor2 == 4 and motor2 == 3)) and (motor2 < 1 or motor2 > 4):
            raise InternalMotorError(
                f"Incompatible Motors {motor} and {motor2}")


def runMotor(motor: int, time: int) -> None:
    ''' Run a motor for a specified period of time (in seconds) '''

    '''
    Create a dictionary that relates motor number to a thread
    if key exists
        if motorThread.is_alive():
            motorThread.running = false
            motorThread should kill itself

    new thread
    '''
    try:
        checkDomain(motor)
    except:
        return

    if motor in motorThreads and motorThreads[motor].is_alive():
        # Update value within thread
        motorThreads[motor].running = False
        
    motorThreads[motor] = MotorThread(motor, time)
    motorThreads[motor].start()


def motorRun(time, motor):
    '''Run the specified motor for a specified amount of time'''
    try:
        checkDomain(motor)
    except:
        return

    # Assuming pillow 1 is left and Pillow 2 is right
    if motor == 1:
        bus.write_byte_data(DEVICE_ADDR, 1, 0xFF)
        bus.write_byte_data(DEVICE_ADDR, 2, 0x00)
    if motor == 2:
        bus.write_byte_data(DEVICE_ADDR, 1, 0x00)
        bus.write_byte_data(DEVICE_ADDR, 2, 0xFF)
    if motor == 3:
        bus.write_byte_data(DEVICE_ADDR, 3, 0xFF)
        bus.write_byte_data(DEVICE_ADDR, 4, 0x00)
    if motor == 4:
        bus.write_byte_data(DEVICE_ADDR, 3, 0x00)
        bus.write_byte_data(DEVICE_ADDR, 4, 0xFF)

    try:
        wait(time, motor)
    except:
        return

    if motor == 1 or motor == 2:
        bus.write_byte_data(DEVICE_ADDR, 1, 0x00)
        bus.write_byte_data(DEVICE_ADDR, 2, 0x00)
    if motor == 3 or motor == 4:
        bus.write_byte_data(DEVICE_ADDR, 3, 0x00)
        bus.write_byte_data(DEVICE_ADDR, 4, 0x00)

    print("motor Finished")


def motorRun2(time, motor, motor2):
    '''Run the specified motors for a specified amount of time'''
    try:
        checkDomain(motor, motor2)
    except:
        return

    # Assuming pillow 1 is left and Pillow 2 is right
    if motor == 1 or motor2 == 1:
        bus.write_byte_data(DEVICE_ADDR, 1, 0xFF)
        bus.write_byte_data(DEVICE_ADDR, 2, 0x00)
    if motor == 2 or motor2 == 2:
        bus.write_byte_data(DEVICE_ADDR, 1, 0x00)
        bus.write_byte_data(DEVICE_ADDR, 2, 0xFF)
    if motor == 3 or motor2 == 3:
        bus.write_byte_data(DEVICE_ADDR, 3, 0xFF)
        bus.write_byte_data(DEVICE_ADDR, 4, 0x00)
    if motor == 4 or motor2 == 4:
        bus.write_byte_data(DEVICE_ADDR, 3, 0x00)
        bus.write_byte_data(DEVICE_ADDR, 4, 0xFF)

    try:
        wait(time, motor, motor2)
    except:
        return

    stopAll()

    print("Motor Finished")


def timeFormat(seconds):
    '''Convert the provided seconds into hours, minutes, seconds'''
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)


class MotorControl:
    # Initalize pin placements and set the pins to output
    # pin 1 inflate pillow 1, pin 2 deflate pillow1, pin 3 inflate pillow 2, pin 4 deflate pillow 2
    def __init__(self):
        self._DEVICE_BUS = 1
        self._DEVICE_ADDR = 0x10
        self._bus = smbus.SMBus(self._DEVICE_BUS)

    def stopAll(self):
        '''Stop all motors'''
        self._bus.write_byte_data(self._DEVICE_ADDR, 1, 0x00)
        self._bus.write_byte_data(self._DEVICE_ADDR, 2, 0x00)
        self._bus.write_byte_data(self._DEVICE_ADDR, 3, 0x00)
        self._bus.write_byte_data(self._DEVICE_ADDR, 4, 0x00)

    # List of predefined functions that control the motors

    def motor1On(self, time):
        self.motorRun(time, 1)

    def motor2On(self, time):
        self.motorRun(time, 2)

    def motor3On(self, time):
        self.motorRun(time, 3)

    def motor4On(self, time):
        self.motorRun(time, 4)

    def motor1Off(self, time):
        self._bus.write_byte_data(self._DEVICE_ADDR, 1, 0x00)

    def motor2Off(self, time):
        self._bus.write_byte_data(self._DEVICE_ADDR, 2, 0x00)

    def motor3Off(self, time):
        self._bus.write_byte_data(self._DEVICE_ADDR, 3, 0x00)

    def motor4Off(self, time):
        self._bus.write_byte_data(self._DEVICE_ADDR, 4, 0x00)

    def inflateAll(self, time):
        self.motorRun2(time, 1, 3)

    def deflateAll(self, time):
        self.motorRun2(time, 2, 4)

    def wait(self, time, motor, motor2=None):
        '''Given a list of motors, wait a specified time and check if they got turned off by something else'''
        for x in range(time):
            if motor2 != None:
                print("motor {} and motor {} on {} second".format(motor, motor2, x))
                if self._bus.read_byte_data(self._DEVICE_ADDR, motor) == 0 or self._bus.read_byte_data(self._DEVICE_ADDR, motor2) == 0:
                    raise MotorStoppedEarlyError("Motor Stopped Early Error")
            else:
                print("motor {} on {} second".format(motor, x))
                if self._bus.read_byte_data(self._DEVICE_ADDR, motor) == 0:
                    raise MotorStoppedEarlyError("Motor Stopped Early Error")
            sleep(1)

    def checkDomain(self, motor, motor2=None):
        '''Check the validity of one or two motors being called'''
        if motor < 1 or motor > 4:
            raise InternalMotorError(f"{motor} is Outside Domain")
        if motor2 != None:
            if ((motor == 1 and motor2 == 2) or (motor == 3 and motor2 == 4) or (motor2 == 2 and motor == 1) or (motor2 == 4 and motor2 == 3)) and (motor2 < 1 or motor2 > 4):
                raise InternalMotorError(
                    f"Incompatible Motors {motor} and {motor2}")

    def runMotor(self, motor: int, time: int) -> None:
        ''' Run a motor for a specified period of time (in seconds) '''
        try:
            self.checkDomain(motor)
        except:
            return

        class MotorThread(Thread):
            def __init__(self, motorControl):
                super().__init__()
                self.motorControl: MotorControl = motorControl

            def run(self):
                # self.motorControl._bus
                print("Starting")
                sleep(5)
                print(f"Done)")

        pass

    def motorRun(self, time, motor):
        '''Run the specified motor for a specified amount of time'''
        try:
            self.checkDomain(motor)
        except:
            return

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

        try:
            self.wait(time, motor)
        except:
            return

        if motor == 1 or motor == 2:
            self._bus.write_byte_data(self._DEVICE_ADDR, 1, 0x00)
            self._bus.write_byte_data(self._DEVICE_ADDR, 2, 0x00)
        if motor == 3 or motor == 4:
            self._bus.write_byte_data(self._DEVICE_ADDR, 3, 0x00)
            self._bus.write_byte_data(self._DEVICE_ADDR, 4, 0x00)

        print("motor Finished")

    def motorRun2(self, time, motor, motor2):
        '''Run the specified motors for a specified amount of time'''
        try:
            self.checkDomain(motor, motor2)
        except:
            return

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

        try:
            self.wait(time, motor, motor2)
        except:
            return

        self.stopAll()

        print("Motor Finished")

    # cycle everything based on given number of loops
    # def cycleLoop(self, inflateTime, deflateTime, waitTime, loopNumber):
    #     totalTime = inflateTime + deflateTime + (waitTime*2-waitTime)
    #     totalLoopTime = totalTime*loopNumber
    #     print("Starting cycle with estimated cycle total time of {}".format(
    #         self.timeFormat(totalLoopTime)))
    #     for i in range(loopNumber):
    #         print("On Loop {}".format(i))
    #         if self.motorRun2(inflateTime, 1, 3) == -2:
    #             break

    #         sleep(waitTime)

    #         if self.motorRun2(deflateTime, 2, 4) == -2:
    #             break
    #         if i < loopNumber-1:
    #             sleep(waitTime)

    def timeFormat(self, seconds):
        '''Convert the provided seconds into hours, minutes, seconds'''
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%d:%02d:%02d" % (hour, minutes, seconds)


class InternalMotorError(Exception):
    '''Catch wrong motor calls'''

    def __init__(self, message):
        super().__init__(message)


class MotorStoppedEarlyError(Exception):
    '''Catch if a motor was premature of its run'''

    def __init__(self, message):
        super().__init__(message)
