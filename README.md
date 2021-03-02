# PillowTalk
#
# Worked on by:
#	Isaac Long
#	Ian Lawrie
#	Javen Zamojcin
# Jacob Allen
# Patrick Janssen
# Advisor:
#	Keith Vertanen
#

Downloads:
STT Engine, waitress


The software requires the hardware of a raspberry pi 3 or 4.

If you do not know how to setup a raspberry pi please follow this tutorial:
https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up

The port that must be used for HTTPS is 443.
The internal and external port might need to be different.

Make sure that the pi is updated and upgraded by using (This will take some time):
sudo apt update
sudo apt full-upgrade

Installations
Flask: sudo pip install -U Flask :https://pypi.org/project/Flask/
sphinx: sudo pip install -U sphinx :https://www.sphinx-doc.org/en/master/usage/installation.html
pybluez: https://github.com/pybluez/pybluez in README
libraries: sudo apt-get install libbluetooth-dev
bluetooth: https://stackoverflow.com/questions/34599703/rfcomm-bluetooth-permission-denied-error-raspberry-pi

Hardware Pin Setup (specific for 4 output signals):

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
than that feeds back to the PI, the board will break.
