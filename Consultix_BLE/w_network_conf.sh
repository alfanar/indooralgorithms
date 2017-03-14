#!/bin/bash

echo "
network={
    ssid=\"${1}\"
    psk=\"${2}\"
}" >> /etc/wpa_supplicant/wpa_supplicant.conf;
sudo ifdown wlan0;
sleep 1;
sudo ifup wlan0;
sleep 1;
