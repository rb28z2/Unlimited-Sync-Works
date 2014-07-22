#!/usr/bin/python2.7

import sys
import os

hashes = open("completed.txt",'r').readlines()
for hash in hashes:
	command = "/home/seedbox/bin/rtcontrol --cull --yes hash=" + hash.strip()
	os.system(command)
os.remove("completed.txt")
