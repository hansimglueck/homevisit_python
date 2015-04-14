#!/usr/bin/env python
#from time import sleep
import time
import os
import RPi.GPIO as GPIO
import ws
import sys
import logging

logging.basicConfig(filename='/button_client.log',level=logging.INFO)
	
cmdargs = str(sys.argv)

gpio_nr = int(sys.argv[1])
sending_param = str(sys.argv[2])
gpio_led_nr = int(sys.argv[3])
instance_name = str(sys.argv[4])

btn_pressed = 0

led_state = 0
### 0 - off
### 1 - on
### 2 - blink
blink_freq = 0
blink_toggle = 0
blink_toggle_timer = 0

# for shutting down the system by holding the white button longer than 5 seconds
stop_timer = time.time()
stop_timer_hold = 0
stop_proc = 0

GPIO.setmode(GPIO.BCM)

def sendGo():
	if not client.conn():
		print("NO GO")
		return
	logging.info("Go")
	print("GO GO GO")
	client.send(type="playbackAction", data="go", param=sending_param)
	os.popen('mpg321 /home/pi/medien/sounds/button-11.mp3 &')
	#client.send(type="forward", data={"type":"display","content":{"text":"mpg321 button-11.mp3"}}, param={"role":"speaker","name":"NN"})
	#client.send(type="forward", data={"type":"display","content":{"command":"countdown","param":10}}, param={"role":"digits","name":"NN"})

def sendShutDown():
	print("System ausschalten!")
	#p.print_text("G O N N A * S L E E P * N O W\n")
	#p.print_text("* * * * * * B Y E * * * * * *\n")
	#p.print_text("-----------------------------\n")

def cb(msg):
	global led_state
	try:
		logging.info("button cb got message")
		print(msg["type"])
		#logging.info("type="+msg["type"]+" - command="+msg["data"]["command"])
		if (msg["type"] == "display"):
			cmd = msg["data"]["type"]
			#print(cmd)
			#if (cmd == "on"):
			#	turnLED_on()
			#elif (cmd == "off"):
			#	turnLED_off()
			#elif (cmd == "blink"):
			#	blink(msg["data"]["param"])
			if (cmd == "alert"):
				al_state = msg["data"]["param"]
				if (al_state == 1):
					turnLED_on()
					#blink(msg["data"]["param"])
				elif (al_state == 2):
					blink(0.3)
				elif (al_state == 0):
					turnLED_off()
			#if (cmd == "off"):
			#	turnLED_off()
	finally:
		print("button cb got message")
			
	
#der client wird in einem extra-thread gestartet...
client = ws.Client(role="button", cb=cb, name=instance_name)

#time.sleep(45)

def turnLED_off():
	global led_state
	global blink_toggle
	#print("LED OFF")
	led_state = 0
	#print(led_state)
	lightOff()
	#GPIO.output(gpio_led_nr, GPIO.LOW)
	blink_toggle = 0
	
def turnLED_on():
	global led_state
	global blink_toggle
	#print("LED ON")
	led_state = 1
	#print(led_state)
	lightOn()
	#GPIO.output(gpio_led_nr, GPIO.HIGH)
	blink_toggle = 0
	
def blink(freq):
	global led_state
	global blink_toggle
	global blink_freq
	global blink_toggle_timer
	#print("LED BLINK")
	led_state = 2
	#print(led_state)
	blink_freq = freq
	if (blink_freq == 0):
		blink_freq = 0.3
	lightOn()
	#GPIO.output(gpio_led_nr, GPIO.HIGH)
	blink_toggle = 1
	blink_toggle_timer = time.time()

def lightOn():
	global sending_param
	GPIO.output(gpio_led_nr, GPIO.HIGH)
	#if(sending_param == "0"):
	#	client.send(type="forward", data={"type":"display","content":{"command":"blink_on","param":0}}, param={"role":"digits","name":"NN"})
	#	print("SEND ON TO DIGITS")

def lightOff():
	global sending_param
	GPIO.output(gpio_led_nr, GPIO.LOW)
	#if(sending_param == "0"):
	#	client.send(type="forward", data={"type":"display","content":{"command":"blink_off","param":0}}, param={"role":"digits","name":"NN"})
	#	print("SEND OFF TO DIGITS")

try:

	GPIO.setup(gpio_nr, GPIO.IN)
	GPIO.setup(gpio_led_nr, GPIO.OUT)

except:
	print("GPIO already in use")
	logging.info("GPIO already in use")
	
else:
	while not stop_proc:
		#print(led_state)
		if ( GPIO.input(gpio_nr) == False):
			if (not btn_pressed):
				### if the button has been pressed
				sendGo()
				#turnLED_off()
				stop_timer = time.time()
				stop_timer_hold = 0
				btn_pressed = 1
				time.sleep(1.5);
			else:
				### if the button is being pressed down longer
				#print(stop_timer_hold)
				stop_timer_hold = time.time() - stop_timer
				if (stop_timer_hold > 5 and not stop_proc):
					stop_proc = 1
		if (GPIO.input(gpio_nr) == True):
			### button is not pressed
			btn_pressed = 0
	
		if (led_state == 2) and ((time.time() - blink_toggle_timer > blink_freq)):
		#if (time.time() - blink_toggle_timer > blink_freq):
			if (blink_toggle == 1):
				lightOff()
				#GPIO.output(gpio_led_nr, GPIO.LOW)
				blink_toggle = 0
				blink_toggle_timer = time.time()
			else:
				lightOn()
				#GPIO.output(gpio_led_nr, GPIO.HIGH)
				blink_toggle = 1
				blink_toggle_timer = time.time()				
		time.sleep(0.1);
	
	if (stop_proc):
		sendShutDown()
		### shutdown system
		command = "/usr/bin/sudo /sbin/shutdown -h now"
		import subprocess
		process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
		output = process.communicate()[0]
		print output

finally: GPIO.cleanup()
