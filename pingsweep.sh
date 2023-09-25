#!/bin/bash
#simple subet scanner written in bash
#if no ip given print
if [ "$1" == "" ]
then
echo "You forgot an IP address!"
echo "Syntax: ./ipsweep.sh 192.168.1"
#for loop ping with 1 count to check if host is up
else
for ip in `seq 1 254`; do
#cut ouput to only return last octet
ping -c 1 $1.$ip | grep "64 bytes" | cut -d " " -f 4 | tr -d ":" &
done
fi
