from  motorControl import *
import traceback

if __name__ == '__main__':
	try:
		motor = MotorControl()
		motor.motorOn(10)
	except KeyboardInterrupt:
		print ("\nwhy did you stop it\n")
	except Exception:
		print ("\nwhy did something else stop it\n")
		traceback.print_exc()
	finally:
		print("done\n")
		GPIO.cleanup()
