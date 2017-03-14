#!/bin/bash


out=${1}

if [ -f $out ];
then
	sudo rm $out;
fi

sudo rm test-accuracy.txt;
echo "Testing instance ---------------------'$(date)'------------------------" &>> "test-accuracy.txt";

for i in {1..10000}
do

	sudo timeout 3s sudo bash Consultix-estimote-scan.sh -b $out;
	nodejs calc_pos.js;
	sudo rm $out;
done
