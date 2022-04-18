# PillowTalk
## Worked on By:
- Isaac Long
- Ian Lawrie
- Javen Zamojcin
- Jacob Allen
- Patrick Janssen
- Michelle Perini
- Josh Overbeek
- Thawng Hmung
- Mark Washington
- Natalia Suwaj
- Liam Cacioppo
- Annika Price

## Advisor: Keith Vertanen

Not Included Downloads:
- STT Engine

**The software requires the hardware of a Raspberry Pi 3 or 4.**

If you do not know how to setup a Raspberry Pi please follow this tutorial:
	https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up

Make sure that the pi is updated and upgraded by using (This will take some time):
```
sudo apt update
sudo apt full-upgrade
```

## New Installation Steps (WIP)
1. Follow the steps at [this link](https://python-poetry.org/docs/#installation) to install the Poetry package manager.
2. Within the project folder run `poetry install`

## Old Installation Steps:
Flask: `sudo pip install -U Flask`
	also found here: https://pypi.org/project/Flask/
	
sphinx: `sudo pip install -U sphinx`
	also found here: https://www.sphinx-doc.org/en/master/usage/installation.html
	
pybluez: `sudo apt-get install libbluetooth-dev`
	also found here: https://github.com/pybluez/pybluez in README libraries

### Bluetooth Permissions:
1. Edit the line `ExecStart=/usr/lib/bluetooth/bluetoothd` under [Service] to `ExecStart=/usr/lib/bluetooth/bluetoothd -C` in /lib/systemd/system/bluetooth.service
2. Copy /lib/systemd/system/bluetooth.service to /etc/systemd/system/bluetooth.service
3. Create the file "/etc/systemd/system/var-run-sdp.path" with
	```
	[Unit]
	Descrption=Monitor /var/run/sdp
		
	[Install]
	WantedBy=bluetooth.service
		
	[Path]
	PathExists=/var/run/sdp
	Unit=var-run-sdp.service
	```
4. Create the file "/etc/systemd/system/var-run-sdp.service" with
	```
	[Unit]
	Description=Set permission of /var/run/sdp

	[Install]
	RequiredBy=var-run-sdp.path
		
	[Service]
	Type=simple
	ExecStart=/bin/chgrp bluetooth /var/run/sdp
	ExecStartPost=/bin/chmod 662 /var/run/sdp
	```		
5. Run the following lines
	```
	sudo systemctl daemon-reload
	sudo systemctl enable var-run-sdp.path
	sudo systemctl enable var-run-sdp.service
	sudo systemctl start var-run-sdp.path
	```	
6. Make sure your pi user is in the bluetooth group:
	`sudo usermod -G bluetooth -a pi`	
7. Reboot the Raspberry Pi.

#### More Reading:
https://stackoverflow.com/questions/34599703/rfcomm-bluetooth-permission-denied-error-raspberry-pi
https://github.com/ev3dev/ev3dev/issues/274#issuecomment-74593671
https://github.com/pybluez/pybluez/issues/390
	
run scripts on startup:

open .bash_login with `sudo nano ~/.bash_login` and enter the follow text:

```
bt_start() {
	sleep 10
	python3 /home/pi/PillowTalk/pillowtalk/BluetoothService.py &
	sleep 1
	python3 /home/pi/PillowTalk/pillowtalk/WebServer.py &
}

bt_start &
cd /home/pi/PillowTalk/newoffline/sopare
python2.7 sopare.py -l &
```

Then run `sudo reboot`
	

waitress: sudo pip install waitress

respeaker: https://github.com/respeaker/seeed-voicecard/issues/192

The port used for local HTTPS is 4433

The external port that must be used for HTTPS is 443.

To run the server, make sure that you are inside of the PillowTalk folder and run "python2.7 web_server.py". This will open the raspberry pi's local ip as a flask server address.
