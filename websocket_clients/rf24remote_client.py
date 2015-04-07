#!/usr/bin/env python
#coding=utf-8

import time
import json
import ws
import logging
from RF24 import *

logging.basicConfig(filename='/remote_client.log',level=logging.DEBUG)

########### RADIO USER CONFIGURATION ###########
# See https://github.com/TMRh20/RF24/blob/master/RPi/pyRF24/readme.md
# CE Pin, CSN Pin, SPI Speed
#RPi B
# Setup for GPIO 15 CE and CE1 CSN with SPI Speed @ 8Mhz
radio = RF24(RPI_V2_GPIO_P1_15, BCM2835_SPI_CS0, BCM2835_SPI_SPEED_8MHZ)
################################################

pipes = [0xF0F0F0F0E1, 0xF0F0F0F0D2]

radio.begin()
radio.enableDynamicPayloads()
radio.setRetries(5,15)
#radio.printDetails()

### receiver pipes
radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1,pipes[0])
radio.startListening()

def cb(msg):
	if (msg["type"] == "display"):
		cmd = msg["data"]["command"]
		#print(cmd)
		if (cmd == "on"):
			print(" ")

#der client wird in einem extra-thread gestartet...
client = ws.Client(role="remote", cb = cb)

def sendGo(nr_string):
	### nr_string is "0" for main button (green), is "1" for second button (red)
	client.send(type="playbackAction", data="go", param=nr_string)
	
def sendRego():
	client.send(type="playbackAction", data="rego")

def sendBack():
	client.send(type="playbackAction", data="back")

def sendAlarmGreen():
	client.send(type="forward", data={"type":"display","content":{"command":"alarm","param":0}}, param={"role":"button","name":"gruen"})

def sendAlarmRed():
	client.send(type="forward", data={"type":"display","content":{"command":"alarm","param":0}}, param={"role":"button","name":"rot"})
	
def sendAlarmBoth():
	sendAlarmGreen()
	sendAlarmRed()

#c = raw_input("Client running.")
while True:
	# Pong back role.  Receive each packet, dump it out, and send it back

	# if there is data ready
	if radio.available():
		while radio.available():
			# Fetch the payload, and see if this was the last one.
			len = radio.getDynamicPayloadSize()
			receive_payload = radio.read(len)

			# Spew it
			#print 'Got payload size=', len, ' value="', receive_payload, '"'
			#sendAlarmGreen()
			sendAlarmBoth()
