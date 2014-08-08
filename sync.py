#!/usr/bin/python

import sys
import os
import vars

#for automation tools because PATH is hard
os.chdir(vars.script_loc)

#receive values
filePath = vars.down_dir + sys.argv[3]
path = sys.argv[1]
hash = sys.argv[2]

if "test/downloads" not in path:
	sys.exit()

#substring the torrent name. If the script throws an exception here later
#on, switch index to find
firstHyphen = sys.argv[3].rfind(' - ')
firstCBrac = sys.argv[3].index(']', 0)
seriesName = sys.argv[3][firstCBrac+2:firstHyphen]
episode = sys.argv[3][firstHyphen+3:]
episode = episode[:episode.index(' ',0)]
filename = seriesName + ' - ' + episode + '.mkv'
print "Series: " + seriesName
print "Episode: " + episode

#open our files of series that we want and make them a list and sort them, and figure out how long
AList = open("A.txt").readlines()
KList = open("K.txt").readlines()
AList.sort()
KList.sort()

#get len just because
ALen = len(AList)
KLen = len(KList)

#set flags (DEATH FLAGS!)
index = 0
hashed = 0
found = "false"

#take each element of the list delete all extra shit and then compare it with the arg passed
#bobstinx

while index < ALen and found == "false":
    searchTerm = AList[index].strip()
    index+=1;

    if searchTerm == seriesName:
        found = "true" 
        command = "rsync --progress -v -z -e 'ssh -p44' \"" + filePath + "\"" + ' ' + "\"" + vars.a_host + ":/cygdrive/f/Anime/Weekly\""
	os.system(command)

	command = "ssh -p44 " + vars.a_host +  " \"mv '/cygdrive/f/Anime/Weekly/" + sys.argv[3] + "' '/cygdrive/f/Anime/Weekly/" + filename + "'\""
        os.system(command)

        command = "echo \'/msg Smoothtalk " + sys.argv[3] + " uploaded and renamed successfully\' > /home/seedbox/.irssi/rc"
        os.system(command)
        command = "echo \'/msg John_Titor " + sys.argv[3] + " uploaded and renamed successfully\' > /home/seedbox/.irssi/rc"
        os.system(command)
	completed = open("completed.txt", "a")
	completed.write(hash)
	completed.write('\n')
	completed.close()
	hashed = 1

#be cheaty and reset flags!
#Can't test this because I don't have a unix to unix connection setup yet
#Will have one soon
found = "false"
index = 0
while index < KLen and found == "false":
    searchTerm = KList[index].strip()
    index+=1

    if searchTerm == seriesName:
        found = true
        command = "rsync --progress -v -z -e 'ssh -p8793' \"" + filePath + "\"" + vars.k_host + ":/home/kanchana/A\""
        os.system(command)

        command = "ssh -p8793 " + vars.k_host + " \"mv '/home/kanchana/A/" + sys.argv[3] + "' '/home/kanchana/A/" + filename + "'\""
        os.system(command)

        command = "echo '/msg localhost " + sys.argv[3] + " uploaded and renamed successfully\' > /home/seedbox/.irssi/rc"
        os.system(command)
	if hashed == 0:
		completed = open("completed.txt", "a")
		completed.write(hash)
		completed.write('\n')
		completed.close()    
