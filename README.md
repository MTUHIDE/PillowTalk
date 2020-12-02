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

Relay 1 is pin 11
Relay 2 is pin 13
Relay 3 is pin 15
Relay 4 is pin 16
Relay 1 is connected to relay 3
Relay 2 is connected to relay 4 

For inflate and deflate of the same cushion, these relays
are connected and either or can be used for inflate or deflate.
If one relay is running then its connected relay cannot run until it is done running.

-------------------------WARNING-----------------------
The output of the GPIO pins is 3.3V and if anything larger
that that feeds back to the PI the board will break.
