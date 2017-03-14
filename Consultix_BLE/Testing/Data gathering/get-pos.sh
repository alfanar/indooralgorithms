#!/bin/bash


out=${1}

if [ -f $out ];
then
	sudo rm $out;
fi

sudo timeout 3s sudo bash Consultix-estimote-scan.sh -b $out;


nodejs calc_pos.js;
