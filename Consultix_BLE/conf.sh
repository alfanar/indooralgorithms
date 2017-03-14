#!/bin/bash

bluezVer=${2}
stage=${1}

error_check(){
	if [ $? != 0 ]
	then
		echo "Error at ${1} $(date)"
		return -1
	fi
}

case $stage in

1)
#update and upgrade RPi
echo "---------------------------------------------------------------update rpi $(date)------------------------------------------------";
sudo apt-get update;
error_check update_rpi;
echo "---------------------------------------------------------------upgrade rpi $(date)------------------------------------------------";
sudo apt-get upgrade -y;
error_check upgrade_rpi;
echo "---------------------------------------------------------------dist-upgrade rpi $(date)------------------------------------------------";
sudo apt-get dist-upgrade -y;
error_check dist-upgrade_rpi;
#install gedit
echo "---------------------------------------------------------------installing gedit $(date)------------------------------------------------";
sudo apt-get install -y gedit;
error_check gedit_install;
echo "---------------------------------------------------------------rpi-update $(date)------------------------------------------------";
sudo rpi-update;
error_check rpi-update;

#rebooting
echo "---------------------------------------------------------------rebooting in 5 minutes $(date)------------------------------------------------";
sleep 300;
sudo reboot;
;;

2)
#install latest bluez version
echo "---------------------------------------------------------------installing bluez specified version $(date)------------------------------------------------";
sudo apt-get install -y git build-essential autoconf cmake libtool libglib2.0 libdbus-1-dev libudev-dev libical-dev libreadline-dev;
sudo wget http://www.kernel.org/pub/linux/bluetooth/bluez-$bluezVer.tar.xz;
error_check bluez_install;
echo "---------------------------------------------------------------tar bluez specified version $(date)------------------------------------------------";
sudo tar xvf bluez-$bluezVer.tar.xz;
error_check tar_bluez;
cd bluez-$bluezVer/;
echo "---------------------------------------------------------------configure and make bluez specified version $(date)------------------------------------------------";
sudo ./configure --prefix=/usr --mandir=/usr/share/man --sysconfdir=/etc --localstatedir=/var --enable-experimental --with-systemdsystemunitdir=/lib/systemd/system --with-systemduserunitdir=/usr/lib/systemd;
error_check bluez_configure;
sudo make;
error_check bluez_make;
sudo make install;
error_check bluez_make_install;
cd /etc/systemd/system/bluetooth.target.wants/;
echo "---------------------------------------------------------------adding --experimental flag to bluez specified version $(date)------------------------------------------------";
(
sudo sed -i -- 's/\/bluetoothd/\/bluetoothd --experimental/g' *bluetooth.service*
)
error_check experimental_flag;
cd;

#patch latest bluez version
echo "---------------------------------------------------------------patching bluez specified version $(date)------------------------------------------------";
cd */bluez-$bluezVer;
sudo wget https://gist.github.com/pelwell/c8230c48ea24698527cd/archive/3b07a1eb296862da889609a84f8e10b299b7442d.zip;
sudo unzip 3b07a1eb296862da889609a84f8e10b299b7442d.zip;
sudo git apply -v c8230c48ea24698527cd-3b07a1eb296862da889609a84f8e10b299b7442d/*;
error_check patching_bluez;
echo "---------------------------------------------------------------configure and make bluez specified version patch $(date)------------------------------------------------";
sudo ./configure --prefix=/usr --mandir=/usr/share/man --sysconfdir=/etc --localstatedir=/var --enable-experimental --with-systemdsystemunitdir=/lib/systemd/system --with-systemduserunitdir=/usr/lib/systemd;
error_check bluez_patch_configure;
sudo make;
sudo make install;
error_check bluea_patch_make;

#rebooting
echo "---------------------------------------------------------------rebooting in 5 minutes $(date)------------------------------------------------";
sleep 300;
sudo reboot;
;;

3)
#install nodejs
echo "---------------------------------------------------------------installing nodejs $(date)------------------------------------------------";
sudo curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
sudo apt-get install -y nodejs;
error_check nodejs_install;

#rebooting
echo "---------------------------------------------------------------rebooting in 5 minutes $(date)------------------------------------------------";
sleep 300;
sudo reboot;
;;

4)
echo "---------------------------------------------------------------installing bluetooth $(date)------------------------------------------------";
sudo apt-get install -y bluetooth libbluetooth-dev libudev-dev;
sudo ln -s /usr/bin/nodejs /usr/bin/node;
error_check bluetooth_install;
echo "---------------------------------------------------------------disable bluetooth $(date)------------------------------------------------";
sudo systemctl disable bluetooth;
error_check disable_bluetooth;
echo "---------------------------------------------------------------config up hci0 $(date)------------------------------------------------";
sudo hciconfig hci0 up;
error_check hci0_up;

echo "---------------------------------------------------------------installing bleacon $(date)------------------------------------------------";
sudo chown -R $USER /usr/local;
npm install bleacon;
npm install async;
npm install prompt;
error_check bleacon_install;

#rebooting
echo "---------------------------------------------------------------rebooting in 5 minutes $(date)------------------------------------------------";
sleep 300;
sudo reboot;
;;

*)
echo "please provide an option"
;;
esac
