#!/usr/bin/env python
import os
import ws

def playSoundfile(filename):
	print filename
	if filename == "stop":
		stopSound()
		return
	os.popen('mpg321 ' + filename + ' &')	

def stopSound():
	os.system('pkill mpg321')

#der client wird in einem extra-thread gestartet...
client = ws.Client(role="radio", cb = playSoundfile)


#damit das programm nicht stoppt
c = raw_input("Client running.")
while 1:
	a = 1

