#!/bin/bash


out=${1}

if [ -f $out ];
then
	sudo rm $out;
fi

for i in {1..8}
do
	sudo nodejs parse-RSSI.js &>> $out;
done

nodejs calc_pos.js;
