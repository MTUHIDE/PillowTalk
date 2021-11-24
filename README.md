# PillowTalk
#
# Worked on by:
#	Isaac Long
#	Ian Lawrie
#	Javen Zamojcin
#       Jacob Allen
#       Patrick Janssen
#   Mark Washington
# Advisor:
#	Keith Vertanen
#

Not Included Downloads:
STT Engine


The software requires the hardware of a raspberry pi 3 or 4.

If you do not know how to setup a raspberry pi please follow this tutorial:

https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up

Make sure that the pi is updated and upgraded by using (This will take some time):

sudo apt update
sudo apt full-upgrade

Installations:

Flask: sudo pip install -U Flask 
	also found here: https://pypi.org/project/Flask/
	
sphinx: sudo pip install -U sphinx
	also found here: https://www.sphinx-doc.org/en/master/usage/installation.html
	
pybluez: https://github.com/pybluez/pybluez in README
libraries: sudo apt-get install libbluetooth-dev

bluetooth permissions:

	1) Edit the line "ExecStart=/usr/lib/bluetooth/bluetoothd" under [Service] to "ExecStart=/usr/lib/bluetooth/bluetoothd -C' in /lib/systemd/system/bluetooth.service
	
	2) Copy /lib/systemd/system/bluetooth.service to /etc/systemd/system/bluetooth.service
	
	3) Create the file "/etc/systemd/system/var-run-sdp.path" with
		[Unit]
		Descrption=Monitor /var/run/sdp
		
		[Install]
		WantedBy=bluetooth.service
		
		[Path]
		PathExists=/var/run/sdp
		Unit=var-run-sdp.service
	
	4) Create the file "/etc/systemd/system/var-run-sdp.service" with
		[Unit]
		Description=Set permission of /var/run/sdp

		[Install]
		RequiredBy=var-run-sdp.path
		
		[Service]
		Type=simple
		ExecStart=/bin/chgrp bluetooth /var/run/sdp
		ExecStartPost=/bin/chmod 662 /var/run/sdp
		
	5) run this
		sudo systemctl daemon-reload
		sudo systemctl enable var-run-sdp.path
		sudo systemctl enable var-run-sdp.service
		sudo systemctl start var-run-sdp.path
		
	6) Make sure your pi user is in the bluetooth group:
		sudo usermod -G bluetooth -a pi
		
	7) Reboot pi
	
	More reading)
	https://stackoverflow.com/questions/34599703/rfcomm-bluetooth-permission-denied-error-raspberry-pi
	https://github.com/ev3dev/ev3dev/issues/274#issuecomment-74593671
	https://github.com/pybluez/pybluez/issues/390
	
run bluethooth_service.py on user login:

	without graphical terminal emulator
	add 'python3 /home/pi/PillowTalk/bluetooth_service.py &' to your bash profile '~/.profile'

	with graphical terminal emulator
	add 'lxterminal -e python3 /home/pi/PillowTalk/bluetooth_service.py &' to your bash profile '~/.profile'
	

waitress: sudo pip install waitress

respeaker: https://github.com/respeaker/seeed-voicecard/issues/192

The port used for local HTTPS is 4433

The external port that must be used for HTTPS is 443.

To run the server, make sure that you are inside of the PillowTalk folder and run "python2.7 web_server.py". This will open the raspberry pi's local ip as a flask server address.

Hardware Pin Setup (specific for 4 output signals):

The output pins can be found using the picture called "GPIO_Pins.png"
with the pin number matching the numbers in the center of the circles.

The output GPIO pins are as follows:

Relay 1 is an inflate on pin 11.
Relay 2 is an inflate on pin 13.
Relay 3 is a deflate on pin 15.
Relay 4 is a deflate on pin 16.
Relay 1 is connected to relay 3.
Relay 2 is connected to relay 4.

The relays that are connected cannot run if one of them is already running.
It cannot inflate and deflate at the same time.

-------------------------WARNING-----------------------

The output of the GPIO pins is 3.3V and if anything larger
than that feeds back to the PI, the board will break.
