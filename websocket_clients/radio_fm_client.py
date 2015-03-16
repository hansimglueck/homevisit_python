#!/usr/bin/env python
import os
import ws
import time

radio_frequency = 100.5

def playSoundfile(filename):
	print filename
	if filename == "stop":
		stopSound()
		return
	os.system('sudo sh /home/pi/homevisit_python/pifmplay/pifmplay ' + filename + ' ' + str(radio_frequency) + ' &>/dev/null &')
	
def stopSound():
	os.system('sudo sh /home/pi/homevisit_python/pifmplay/pifmplay stop')

#der client wird in einem extra-thread gestartet...
client = ws.Client(role="radio", cb = playSoundfile)


#damit das programm nicht stoppt
c = raw_input("Client running.")
while 1:
	time.sleep(1)

