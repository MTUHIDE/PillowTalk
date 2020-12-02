# PillowTalk

# Worked on by:
#	Isaac Long
#	Ian Lawrie
#	Javen Zamojcin

Hardware Pin Setup (specific for 4 output signals):

The software requires the hardware of a raspberry pi 3 or 4.

The output pins can be found using the picture called "GPIO_Pins.png"
with the pin number matching the numbers in the center of the circles.

The output GPIO pins are as follows:

Relay 1 is an inflate on pin 11
Relay 2 is an inflate on pin 13
Relay 3 is a deflate on pin 15
Relay 4 is a deflate on pin 16
Relay 1 is connected to relay 3
Relay 2 is connected to relay 4 

The relays that are connected cannot run if one of them is already running.
It cannot inflate and deflate at the same time.

-------------------------WARNING-----------------------
The output of the GPIO pins is 3.3V and if anything larger
that that feeds back to the PI the board will break.
