#!/usr/bin/python

import time
import ws
import logging 
from Adafruit_7Segment import SevenSegment
logging.basicConfig(filename='/digit_client.log',level=logging.DEBUG)

# ===========================================================================
# ===========================================================================

segment = SevenSegment(address=0x74)
time_whole = 10
now = time_whole
mode = ""

digit_0 = 0
digit_1 = 0
digit_3 = 0
digit_4 = 0
colon = 0

#print "Press CTRL+Z to exit"


def turnOff():
	global segment
	segment.writeDigitRaw(0, 0)
	segment.writeDigitRaw(1, 0)
	segment.writeDigitRaw(3, 0)
	segment.writeDigitRaw(4, 0)
	segment.setColon(0) 

def turnOn():
        global segment
        segment.writeDigit(0, 8)
        segment.writeDigit(1, 8)
        segment.writeDigit(3, 8)
        segment.writeDigit(4, 8)
        segment.setColon(1)

def cb(msg):
	global mode
	logging.info("digits cb got message")
	logging.info("type="+msg["type"]+" - command="+msg["data"]["command"])
	#print("DIGITS GETS MSG TYPE: " + msg["type"])
	if (msg["type"] == "display"):
		cmd = msg["data"]["command"]
		#print("DIGITS GETS CMD: " + cmd)
		if (cmd == "countdown"):
			countdown(int(msg["data"]["param"]))
		elif (cmd == "blink_on"):
			#print("DIGITS ON")
			blink(1)
		elif (cmd == "blink_off"):
			#print("DIGITS ON")
			blink(0)

def countdown(secs):
	global mode
	global now
	global time_whole
	logging.info("Set digits to countdown: " + str(secs))
	sendSound("mpg321 /home/pi/medien/sounds/uhr_ticken.mp3 --loop 0")
	mode = "countdown"
	time_whole = secs
	now = time_whole

def blink(onoroff):
	global mode
	#logging.info("Set digits to blink: " + str(onoroff))
	if (onoroff == 0):
		if (mode != "countdown"):
			turnOff()
			mode = "blink"
	elif (onoroff == 1):
		if (mode != "countdown"):
			turnOn()
			mode = "blink"
		sendSound("mpg321 /home/pi/medien/sounds/alarm.mp3")


def sendSound(filepath):
	client.send(type="forward", data={"type":"display","content":{"text":filepath}}, param={"role":"speaker","name":"NN"})

#der client wird in einem extra-thread gestartet...
client = ws.Client(role="digits", cb = cb)

turnOff()

while(True):
	#print(mode)
	if (mode == "countdown"):
		if (now > 0):
			now = now - 1
			# Minutes
			minutes = int(now / 60)
			digit_0 = int(minutes / 10)
			digit_1 = minutes % 10
			# Seconds
			seconds = now % 60
			digit_3 = int(seconds / 10)
			digit_4 = seconds % 10
			# Toggle colon at 1Hz
			colon = now % 2

			#logging.info(digit_0)
			#logging.info(digit_1)
			#logging.info(digit_3)
			#logging.info(digit_4)
			#logging.info(":::::::")
		else:
			# countdown complete
			mode = ""
			sendSound("stopmpg321")
			sendSound("mpg321 /home/pi/medien/sounds/time_up.mp3")
	if (mode == ""):
		turnOff()
	elif (mode == "countdown"):
		# Set digits
		segment.writeDigit(0, digit_0)
		segment.writeDigit(1, digit_1)
		segment.writeDigit(3, digit_3)
		segment.writeDigit(4, digit_4)
		# Set colon
		segment.setColon(colon)

	# Wait one second
	time.sleep(1)

