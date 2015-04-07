#!/usr/bin/env python
import time
import os
import ws
import logging
logging.basicConfig(filename='/speaker_client.log',level=logging.DEBUG)

def playSoundfile(msg):
        if msg["type"] != "display":
                return
        filename = msg["data"]["text"] 
	print filename
	if filename == "stop":
		stopSound()
		return
	elif filename == "stopmpg321":
		stopmpg321()
		return
	elif filename.startswith( 'mpg321 ' ):
		filename = filename[7:];
		os.popen('mpg321 ' + filename + ' &')
	else:
		os.popen('omxplayer ' + filename + ' &')

def stopSound():
	os.system("sudo pkill omxplayer");

def stopmpg321():
        os.system('pkill mpg321')

#der client wird in einem extra-thread gestartet...
client = ws.Client(role="speaker", cb = playSoundfile)


#damit das programm nicht stoppt
#c = raw_input("Client running.")
while True:
	time.sleep(1)

