import os

radio_frequency = 100.5

def playSoundfile(filename):
	os.system('sudo sh pifmplay/pifmplay ' + filename + ' ' + str(radio_frequency) + ' &>/dev/null &')
	
def stopSound():
	os.system('sudo sh pifmplay/pifmplay stop')
