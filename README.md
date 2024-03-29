# PillowTalk
## Members
- **Dr. Keith Vertanen (Advisor)**
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

## Setting Up the Raspberry Pi
Not Included Downloads:
- STT Engine

**The software requires the hardware of a Raspberry Pi 3 or 4.**

If you do not know how to setup a Raspberry Pi please follow this tutorial:
	https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up

Make sure that the Pi is updated and upgraded with the following commands, which *will take some time*:
```
sudo apt update
sudo apt full-upgrade
```

## New Installation Steps (WIP)
1. Follow the steps at [this link](https://python-poetry.org/docs/#installation) to install the Poetry package manager.
2. Within the project folder run `poetry install`

## Old Installation Steps
Flask: `sudo pip install -U Flask`
	also found here: https://pypi.org/project/Flask/
	
sphinx: `sudo pip install -U sphinx`
	also found here: https://www.sphinx-doc.org/en/master/usage/installation.html
	
pybluez: `sudo apt-get install libbluetooth-dev`
	also found here: https://github.com/pybluez/pybluez in README libraries

### Bluetooth Permissions:
1. Edit the line `ExecStart=/usr/lib/bluetooth/bluetoothd` under [Service] to `ExecStart=/usr/lib/bluetooth/bluetoothd -C` in **/lib/systemd/system/bluetooth.service**
2. Copy **/lib/systemd/system/bluetooth.service** to **/etc/systemd/system/bluetooth.service**
3. Create the file **/etc/systemd/system/var-run-sdp.path** with
	```
	[Unit]
	Descrption=Monitor /var/run/sdp
		
	[Install]
	WantedBy=bluetooth.service
		
	[Path]
	PathExists=/var/run/sdp
	Unit=var-run-sdp.service
	```
4. Create the file **/etc/systemd/system/var-run-sdp.service** with
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
5. Run the following commands
	```
	sudo systemctl daemon-reload
	sudo systemctl enable var-run-sdp.path
	sudo systemctl enable var-run-sdp.service
	sudo systemctl start var-run-sdp.path
	```	
6. Make sure your Pi user is in the Bluetooth group:
	`sudo usermod -G bluetooth -a pi`	
7. Reboot the Raspberry Pi.

#### More Reading:
- https://stackoverflow.com/questions/34599703/rfcomm-bluetooth-permission-denied-error-raspberry-pi
- https://github.com/ev3dev/ev3dev/issues/274#issuecomment-74593671
- https://github.com/pybluez/pybluez/issues/390
	
### Run Scripts on Startup:
open .bash_login with `sudo nano ~/.bash_login` and enter the following text:
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
	
Install Waitress with the following command: `sudo pip install waitress`

respeaker: https://github.com/respeaker/seeed-voicecard/issues/192

### How to Run:
If start script does not work, `cd PillowTalk` then run `python3 pillowtalk/WebServer.py &`. Any other script can now be run.

To initialize bluetooth service run `python3 pillowtalk/BluetoothService.py &`.

To run speech to text, `cd newoffline/sopare` then run `python2.7 sopare.py -l &`

This will open the Raspberry Pi's local IP as a flask server address.

The port used is **3000**.

Connect to web application by using address `localhost:3000`
