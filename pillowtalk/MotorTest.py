from TextParser import *
from MotorControl import *

if __name__ == "__main__":
	try:
		motorControl = MotorControl()
		print(motorControl.relayRun(5, 1))
		print(motorControl.relayRun(5, 2))
		print(motorControl.relayRun(5, 3))
		print(motorControl.relayRun(5, 4))
	except KeyboardInterrupt:
		print("stopped")
		motorControl.stopAll()
