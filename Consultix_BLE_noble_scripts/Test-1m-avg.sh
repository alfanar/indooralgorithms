#!/bin/bash

if [ -f "test-mean.txt" ];
then
	sudo rm "test-mean.txt";
fi

for i in {1..10000}
do
	sudo nodejs parse-RSSI.js &>> "test-mean.txt";
done
echo "Testing instance ---------------------'$(date)'------------------------" &>> "test-mean-results.txt";
sudo nodejs calc-avg-rssi.js &>> "test-mean-results.txt";
