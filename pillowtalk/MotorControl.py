from time import sleep

from threading import Thread, Lock

import smbus

"""
ID 1 and 2 are for pillow 1 control, ID 1 for inflating and ID 2 for deflating
ID 3 and 4 are for pillow 2 control, ID 3 for inflating and ID 4 for Deflating
0x00 is OFF
0xFF is ON
"""

DEVICE_BUS = 1
DEVICE_ADDR = 0x10

OFF = 0x00
ON = 0xFF

bus = smbus.SMBus(DEVICE_BUS)

# Concurrency stuff
# Dict to relate motor num to a thread for that motor
motorThreads = {}

# Prevents multiple requests from editing the thread dict at the same time
runMotorLock = Lock()


class MotorThread(Thread):

    def __init__(self, motor: int, timeout: int):
        super().__init__()
        self.motor = motor

        # Multiply timeout by 4 to sleep in quarter second increments for better responsiveness
        self.timeout = timeout * 4
        self.running = True

    def run(self):
        '''
        Main function for a motor thread. Enables a motor and disables its complement, then loops repeatedly until time has elapsed.
        '''

        # Determine which motor to turn off, e.g. turn off motor 1 if 2 is turned on
        self.offMotor = self.motor - 1 if self.motor % 2 == 0 else self.motor + 1
        print(
            f"Started thread for motor {self.motor}, turning off motor {self.offMotor}")

        # Send commands to bus to enable/disable motors
        bus.write_byte_data(DEVICE_ADDR, self.motor, ON)
        bus.write_byte_data(DEVICE_ADDR, self.offMotor, OFF)

        # Loop until timeout has ended and while the thread is still supposed to be running
        while (self.timeout > 0 and self.running):
            # Check if the motor this thread is controlling has been turned off by something
            if bus.read_byte_data(DEVICE_ADDR, self.motor) == 0:
                print(f"Motor {self.motor} stopped early for some reason")
                break

            sleep(0.25)
            self.timeout -= 1

        # Turn this thread's motor off
        bus.write_byte_data(DEVICE_ADDR, self.motor, OFF)

    def stop(self):
        '''
        Tell this thread to stop
        '''

        self.running = False


def stopAll():
    '''Stop all motors by setting each hexadecimal value to 0x00.'''
    bus.write_byte_data(DEVICE_ADDR, 1, OFF)
    bus.write_byte_data(DEVICE_ADDR, 2, OFF)
    bus.write_byte_data(DEVICE_ADDR, 3, OFF)
    bus.write_byte_data(DEVICE_ADDR, 4, OFF)


def motor1On(time):
    '''Run motor 1 over a given time interval.'''
    motorRun(time, 1)


def motor2On(time):
    '''Run motor 2 over a given time interval.'''
    motorRun(time, 2)


def motor3On(time):
    '''Run motor 3 over a given time interval.'''
    motorRun(time, 3)


def motor4On(time):
    '''Run motor 4 over a given time interval.'''
    motorRun(time, 4)


def motor1Off():
    '''Stop motor 1 by setting its hexadecimal value to 0x00.'''
    bus.write_byte_data(DEVICE_ADDR, 1, OFF)


def motor2Off():
    '''Stop motor 2 by setting its hexadecimal value to 0x00.'''
    bus.write_byte_data(DEVICE_ADDR, 2, OFF)


def motor3Off():
    '''Stop motor 3 by setting its hexadecimal value to 0x00.'''
    bus.write_byte_data(DEVICE_ADDR, 3, OFF)


def motor4Off():
    '''Stop motor 4 by setting its hexadecimal value to 0x00.'''
    bus.write_byte_data(DEVICE_ADDR, 4, OFF)


def inflateAll(time):
    '''Run motors 1 and 3 over a given time interval to inflate both pillows.'''
    motorRun2(time, 1, 3)


def deflateAll(time):
    '''Run motors 2 and 4 over a given time interval to deflate both pillows.'''
    motorRun2(time, 2, 4)


def wait(time, motor, motor2=None):
    '''
    Given a list of motors, wait a specified time and check if they got turned off by something else
    '''

    for x in range(time):
        if motor2 != None:
            print(f"Motor {motor} and motor {motor2} on for {x} second(s)")
            if bus.read_byte_data(DEVICE_ADDR, motor) == 0 or bus.read_byte_data(DEVICE_ADDR, motor2) == 0:
                raise MotorStoppedEarlyError("Motor Stopped Early Error")
        else:
            print(f"Motor {motor} on for {x} second(s)")
            if bus.read_byte_data(DEVICE_ADDR, motor) == 0:
                raise MotorStoppedEarlyError("Motor Stopped Early Error")
        sleep(1)


def checkDomain(motor, motor2=None):
    '''
    Check the validity of one or two motors being called
    '''

    if motor < 1 or motor > 4:
        raise InternalMotorError(f"{motor} is outside domain")
    if motor2 != None:
        if ((motor == 1 and motor2 == 2) or (motor == 3 and motor2 == 4) or (motor2 == 2 and motor == 1) or (motor2 == 4 and motor2 == 3)) and (motor2 < 1 or motor2 > 4):
            raise InternalMotorError(
                f"Incompatible Motors {motor} and {motor2}")


def runMotor(motor: int, time: int) -> None:
    '''
    Spawn a new thread to run a motor for a specified amount of time
    '''

    # Make sure the motor is within the possible range
    checkDomain(motor)

    print(f"Creating thread for motor {motor}")

    # Lock the mutex to prevent threads from being created simultaneously
    runMotorLock.acquire()

    # Check if a thread exists already for a motor, if so tell it to stop and wait for it to stop
    if motor in motorThreads:
        motorThreads[motor].stop()
        motorThreads[motor].join()

    # Create a new thread and start it
    motorThreads[motor] = MotorThread(motor, time)
    motorThreads[motor].start()

    # Release the mutex so more threads can be created
    runMotorLock.release()


def motorRun(time, motor):
    '''
    Run the specified motor for a specified amount of time
    '''

    try:
        checkDomain(motor)
    except:
        return

    # Assuming pillow 1 is left and Pillow 2 is right
    if motor == 1:
        bus.write_byte_data(DEVICE_ADDR, 1, ON)
        bus.write_byte_data(DEVICE_ADDR, 2, OFF)
    if motor == 2:
        bus.write_byte_data(DEVICE_ADDR, 1, OFF)
        bus.write_byte_data(DEVICE_ADDR, 2, ON)
    if motor == 3:
        bus.write_byte_data(DEVICE_ADDR, 3, ON)
        bus.write_byte_data(DEVICE_ADDR, 4, OFF)
    if motor == 4:
        bus.write_byte_data(DEVICE_ADDR, 3, OFF)
        bus.write_byte_data(DEVICE_ADDR, 4, ON)

    try:
        wait(time, motor)
    except:
        return

    if motor == 1 or motor == 2:
        bus.write_byte_data(DEVICE_ADDR, 1, OFF)
        bus.write_byte_data(DEVICE_ADDR, 2, OFF)
    if motor == 3 or motor == 4:
        bus.write_byte_data(DEVICE_ADDR, 3, OFF)
        bus.write_byte_data(DEVICE_ADDR, 4, OFF)

    print("motor Finished")


def motorRun2(time, motor, motor2):
    '''
    Run the specified motors for a specified amount of time
    '''

    checkDomain(motor, motor2)

    # Assuming pillow 1 is left and Pillow 2 is right
    if motor == 1 or motor2 == 1:
        bus.write_byte_data(DEVICE_ADDR, 1, ON)
        bus.write_byte_data(DEVICE_ADDR, 2, OFF)
    if motor == 2 or motor2 == 2:
        bus.write_byte_data(DEVICE_ADDR, 1, OFF)
        bus.write_byte_data(DEVICE_ADDR, 2, ON)
    if motor == 3 or motor2 == 3:
        bus.write_byte_data(DEVICE_ADDR, 3, ON)
        bus.write_byte_data(DEVICE_ADDR, 4, OFF)
    if motor == 4 or motor2 == 4:
        bus.write_byte_data(DEVICE_ADDR, 3, OFF)
        bus.write_byte_data(DEVICE_ADDR, 4, ON)

    try:
        wait(time, motor, motor2)
    except:
        return

    stopAll()

    print("Motor Finished")


def timeFormat(seconds):
    '''
    Convert the provided seconds into hours, minutes, seconds
    '''

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
