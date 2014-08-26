#!/usr/bin/python

import sys
import os
import retMal
import vars
import xml.etree.ElementTree as ET

#for automation tools because PATH is hard
os.chdir(vars.script_loc)

#change sys.argv[1] to renamed
filePath = vars.host_download_dir + sys.argv[3]
path = sys.argv[1]
hash = sys.argv[2]
hashed = 0

#Need to work on this
#if "test/downloads" not in path: 
#    sys.exit()

#substring the torrent name. If the scrip throws an exception here later
#on, switch index to find
firstHyphen = sys.argv[3].rfind(' - ')
firstCBrac = sys.argv[3].index(']', 0)
seriesName = sys.argv[3][firstCBrac+2:firstHyphen]
episode = sys.argv[3][firstHyphen+3:]
episode = episode[:episode.index(' ',0)]
filename = seriesName + ' - ' + episode + '.mkv'
print "Series: " + seriesName
print "Episode: " + episode

user_len = len(vars.usernames)
x = 0

#load flags for a new user
#switch this to a while loop
while (x <= user_len - 1):
    found = "false"

    command = "python retMal.py " + '\"' + vars.usernames[x] + '\"'
    os.system(command)
    file_input = open("flags", 'rb')
    
    exists = file_input.read(1)
    database = vars.usernames[x] + ".xml"
    
#take each element of the list delete all extra shit and then compare it with the arg passed
#working on pure vars.py for universal use
#bobstinx

    if exists == '0':
        sys.exit()
    else:
        with open(database, 'rt') as f:
            tree = ET.parse(f)
            
            for node in tree.findall('.//anime'):
                raw_status = node.find('my_status').text
                status = raw_status.strip()
                
                if status == '1':
                    raw_title = node.find('series_title').text
                    raw_alt_title = node.find('series_synonyms').text #this is a list
                    raw_my_watched_episodes = node.find('my_watched_episodes').text
                    
                    title = raw_title.strip()
                    alt_title_unsplit = raw_alt_title.strip()
                    alt_title = alt_title_unsplit.split('; ')
                    my_watched_episodes = raw_my_watched_episodes.strip()

                    for element in alt_title:
                        if element != '' and found == "false":
                            if title == seriesName or element == seriesName:
                                if x == 0:
                                    found = "true"
                                    command = "rsync --progress -v -z -e 'ssh -p" + vars.userport1 + "'" + " \"" + filePath + "\"" + ' ' + "\"" + vars.a_host + ":" + vars.remote_download_dir1 + "\""
                                    os.system(command)                   
                                    command = "ssh -p" + vars.userport1 + ' ' + vars.a_host +  " \"mv '" + vars.remote_download_dir1 +  sys.argv[3] + "' '" + vars.remote_download_dir1 + filename + "'\""
                                    #Put reaction that you want if anime is found in user1's list
                                elif x == 1:
                                    found = "true"
                                    command = "rsync --progress -v -z -e 'ssh -p" + vars.userport2 + "'" + " \"" + filePath + "\"" + ' ' + "\"" + vars.k_host + ":" + vars.remote_download_dir2 + "\""
                                    os.system(command)
                                    command = "ssh -p" + vars.userport2 + ' ' + vars.k_host +  " \"mv '" + vars.remote_download_dir2 +  sys.argv[3] + "' '" + vars.remote_download_dir2 + filename + "'\""
                                    os.system(command)
                                    #Put reaction that you want if anime is found in user2's list

                                if hashed == 0:
                                    completed = open("completed.txt", "a")
                                    completed.write(hash)
                                    completed.write('\n')
                                    completed.close()
                                    hashed = 1
                                elif x == 1:
                                    if hashed == 0:
                                        completed = open("completed.txt", "a")
                                        completed.write(hash)
                                        completed.write('\n')
                                        completed.close()
    x = x + 1
    command = "rm flags"
    os.system(command)
