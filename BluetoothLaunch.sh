# Script for launching the bluetooth server on Pi startup
# Navigate home, then to the directory containing the script, then home again

cd /
cd home/pi/PillowTalk # file location
python3 bluetooth_service.py # replace this with seperate launch script if we decide to do that
cd /

# make script available with chmod "755 BluetoothLaunch.sh"
# test with sh BluetoothLaunch.sh

# make log directory with mkdir logs
# open crontab with "sudo crontab -e"
# enter the following to trigger the script on boot
# "@reboot sh /(path to BluetoothLaunch.sh) > /(path to logs dir)/logs/cronlog 2>&1

# BEFORE SETTING IT UP ON START: make sure we can force exit if we want to
