#!/usr/bin/env python
import time
import os
import ws
import logging
logging.basicConfig(filename='speaker_client.log',level=logging.DEBUG)

def playSoundfile(filename):
	print filename
	if filename == "stop":
		stopSound()
		return
	os.popen('mpg321 ' + filename + ' &')	

def stopSound():
	os.system('pkill mpg321')

#der client wird in einem extra-thread gestartet...
client = ws.Client(role="speaker", cb = playSoundfile)


#damit das programm nicht stoppt
#c = raw_input("Client running.")
while True:
	time.sleep(1)

