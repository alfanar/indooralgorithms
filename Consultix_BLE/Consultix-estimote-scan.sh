#!/bin/bash

opt="${1}"
file1="${2}"
file2="${3}"

hciconfig hci0 down;
hciconfig hci0 up;

case $opt in

	-a) nodejs estimote.js
	;;

	-b) echo "Logging output in $file1 - Ctrl+C to stop ..."
	echo "scanning instance ---------------------'$(date)'------------------------" &>> $file1
	nodejs estimote.js &>> $file1
	;;

	-c) echo "Logging HCI traffic in $file2"
	echo "scanning instance ---------------------'$(date)'------------------------" &>> $file2
	hcidump &>> $file2 & # logging the HCI traffic to specified file
	echo "Logging output in $file1 - Ctrl+C to stop ..."
	echo "scanning instance ---------------------'$(date)'------------------------" &>> $file1
	nodejs estimote.js &>> $file1 && fg
	;;

	-d) nodejs /home/pi/node_modules/bleacon/estimote/Consultix-ble-est.js;
	;;

	-e) echo "Logging output in $file1 - Ctrl+C to stop ..."
	echo "scanning instance ---------------------'$(date)'------------------------" &>> $file1
	nodejs /home/pi/node_modules/bleacon/estimote/Consultix-ble-est.js &>> $file1
	echo "Finished logging!"
	;;

	-f) echo "Logging HCI traffic in $file2"
	echo "scanning instance ---------------------'$(date)'------------------------" &>> $file2
	hcidump &>> $file2 & # logging the HCI traffic to specified file
	echo "Logging output in $file1 - Ctrl+C to stop ..."
	echo "scanning instance ---------------------'$(date)'------------------------" &>> $file1
	nodejs /home/pi/node_modules/bleacon/estimote/Consultix-ble-est.js &>> $file1 &&
	echo "Finished Logging!"
	;;

	-g) while [ 1 ]
	do
		hciconfig hci0 reset
		timeout --preserve-status --foreground 10s hcitool lescan # LEscan using modified hcitool to get rssi
	done
	;;

	-h) echo "Logging output in $file1 - Ctrl+C to stop ..."
	echo "scanning instance ---------------------'$(date)'------------------------" &>> $file1
	while [ 1 ]
	do
		hciconfig hci0 reset
		timeout --preserve-status --foreground 20s hcitool lescan &>> $file1 # LEscan using modified hcitool to get rssi
	done
	;;

	-i) echo "Logging HCI traffic in $file2"
	echo "scanning instance ---------------------'$(date)'------------------------" &>> $file2
	hcidump &>> $file2 & # logging the HCI traffic to specified file
	echo "Logging output in $file1 - Ctrl+C twice to stop ..."
	echo "scanning instance ---------------------'$(date)'------------------------" &>> $file1
	while [ 1 ]
	do
		hciconfig hci0 reset
		timeout --preserve-status --foreground 20s hcitool lescan &>> $file1 # LEscan using modified hcitool to get rssi
	done && fg
	;;

	-j) while [ 1 ]
	do
		hciconfig hci0 reset
		hcitool cmd 0x08 0x000c 0x01 0x01 # LEscan using defined device (direct HCI command)
	done
	;;

	-k) echo "Logging HCI traffic in $file1 - Ctrl+C to stop ..."
	echo "scanning instance ---------------------'$(date)'------------------------" &>> $file1
	while [ 1 ]
	do
		hciconfig hci0 reset
		hcitool cmd 0x08 0x000c 0x01 0x01 &>> $file1 # LEscan using defined device (direct HCI command)
	done
	;;

	-L) echo ""
	echo "Please wait to enter the new desired Advertisement Interval..."
	nodejs /home/pi/node_modules/bleacon/estimote/W_Adv_int.js;
	;;

	-M) echo ""
	echo "Please wait to enter the new desired Major..."
	nodejs /home/pi/node_modules/bleacon/estimote/W_Major.js;
	;;

	-N) echo ""
	echo "Please wait to enter the new desired Minor..."
	nodejs /home/pi/node_modules/bleacon/estimote/W_Minor.js;
	;;

	*) echo "${0} use: sudo bash ${0} [option] [file_1] [file_2]"
		echo "or sudo bash ${0} [option]"
		echo ""
		echo "options"
		echo ""
		echo "-a             use bleacon for genaral iBeacon scanning"
		echo "               output: stdout scanning logs with {uuid,MAC,major,minor,powerLevel,rssi,accuracy,proximity[immediate,near,far]}"
		echo ""
		echo "-b             use bleacon for general iBeacon scanning - log output to [file_1]"
		echo "               output: scanning logs with {uuid,MAC,major,minor,powerLevel,rssi,accuracy,proximity[immediate,near,far]}"
		echo ""
		echo "-c             use bleacon for general iBeacon scanning - log output to [file_1] - log HCI traffic to [file_2]"
		echo "               output: scanning logs with {uuid,MAC,major,minor,powerLevel,rssi,accuracy,proximity[immediate,near,far]} in [file_1]"
		echo "                       HCI commands and events traffic logs in [file_2]"
		echo ""
		echo "-d             use bleacon for Estimote Beacon scanning"
		echo "               output: stdout scanning logs with {MAC,major,minor,uuid1,uuid2,powerLevel,advertisment interval,temperature,service 2_9, service 2_10,Battery level,Service Configuration,Firmware version,Hardware version}"
		echo ""
		echo "-e             use bleacon for Estimote Beacon scanning - log output to [file_1]"
		echo "               output: scanning logs with {MAC,major,minor,uuid1,uuid2,powerLevel,advertisment interval,temperature,service 2_9, service 2_10,Battery level,Service Configuration,Firmware version,Hardware version} in [file_1]"
		echo ""
		echo "-f             use bleacon for Estimote Beacon scanning - log output to [file_1] - log HCI traffic to [file_2]"
		echo "               output: scanning logs with {MAC,major,minor,uuid1,uuid2,powerLevel,advertisment interval,temperature,service 2_9, service 2_10,Battery level,Service Configuration,Firmware version,Hardware version} in [file_1]"
		echo "                       HCI commands and events traffic logs in [file_2]"
		echo ""
		echo "-g             use modified hcitool lescan command"
		echo "               output: stdout scanning logs with {MAC,name,rssi}"
		echo ""
		echo "-h             use modified hcitool lescan command - log output to [file_1]"
		echo "               output: stdout scanning logs with {MAC,name,rssi} in [file_1]"
		echo ""
		echo "-i             use modified hcitool lescan command - log output to [file_1] - log HCI traffic to [file_2]"
		echo "               output: stdout scanning logs with {MAC,name,rssi} in [file_1]"
		echo "                       HCI commands and events traffic logs in [file_2]"
		echo ""
		echo "-j             use HCI direct lescan command"
		echo "               output: stdout scanning logs, some tailed with RSSI"
		echo ""
		echo "-k             use HCI direct lescan command - log output to [file_1]"
		echo "               output: scanning logs, some tailed with RSSI in [file_1]"
		echo ""
		echo "-L             use bleacon estimote to edit and/or view the Advertisment interval"
		echo "               output: prompt to insert the new Adv. Int. in milliseconds, then showing the current and last Adv. Int."
		echo "               note: to work properly W_Adv_int.js file must be copied to the /noble-modules/bleacon/estimote/ directory"
		echo ""
		echo "-M             use bleacon estimote to edit and/or view the Minor"
		echo "               output: prompt to insert the new Major, then showing the current and last Major"
		echo "               note: to work properly W_Major.js file must be copied to the /noble-modules/bleacon/estimote/ directory"
		echo ""
		echo "-N             use bleacon estimote to edit and/or view the Major"
		echo "               output: prompt to insert the new Minor, then showing the current and last Minor"
		echo "               note: to work properly W_Minor.js file must be copied to the /noble-modules/bleacon/estimote/ directory"
	;;
esac
