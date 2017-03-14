#!/bin/bash

if [ -f "test-accuracy.txt" ];
then
	sudo rm "test-accuracy.txt";
fi

echo "Testing instance ---------------------'$(date)'------------------------" &>> "test-accuracy.txt";
for i in {1..10000}
do
	sudo bash tri.sh out.txt &>> "test-accuracy.txt";
done
