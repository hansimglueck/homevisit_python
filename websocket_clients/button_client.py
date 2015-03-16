#!/usr/bin/env python
#from time import sleep
import time
import os
import RPi.GPIO as GPIO
import ws
import sys
import logging

try:

	logging.basicConfig(filename='button_client.log',level=logging.DEBUG)
	
	cmdargs = str(sys.argv)
	
	gpio_nr = int(sys.argv[1])
	sending_param = str(sys.argv[2])
	gpio_led_nr = int(sys.argv[3])
	instance_name = str(sys.argv[4])
	
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(gpio_nr, GPIO.IN)
	GPIO.setup(gpio_led_nr, GPIO.OUT)
	
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
	
	def sendGo():
		if not client.conn():
			print("NO GO")
			return
		logging.info("Go")
		print("GO GO GO")
		client.send(type="playbackAction", data="go", param=sending_param)
	
	def sendShutDown():
		print("System ausschalten!")
		#p.print_text("G O N N A * S L E E P * N O W\n")
		#p.print_text("* * * * * * B Y E * * * * * *\n")
		#p.print_text("-----------------------------\n")
	
	def cb(msg):
		if (msg["type"] == "button_led"):
			cmd = msg["data"]["command"]
			if (cmd == "on"):
				turnLED_on()
			elif (cmd == "off"):
				turnLED_off()
			elif (cmd == "blink"):
				blink(msg["data"]["param"])
			elif (cmd == "alarm"):
				if (led_state == 0):
					turnLED_on()
				elif (led_state == 1):
					blink(msg["data"]["param"])
				elif (led_state == 2):
					turnLED_off()
				
		
	#der client wird in einem extra-thread gestartet...
	client = ws.Client(role="button", cb=cb, name=instance_name)
	
	#time.sleep(45)
	
	def turnLED_off():
		led_state = 0
		GPIO.output(gpio_led_nr, GPIO.LOW)
		blink_toggle = 0
		
	def turnLED_on():
		led_state = 1
		GPIO.output(gpio_led_nr, GPIO.HIGH)
		blink_toggle = 0
		
	def blink(freq):
		led_state = 2
		blink_freq = freq
		if (blink_freq == 0):
			blink_freq = 0.5
		GPIO.output(gpio_led_nr, GPIO.HIGH)
		blink_toggle = 1
		blink_toggle_timer = time.time()
	
	while not stop_proc:
		if ( GPIO.input(gpio_nr) == False):
			if (not btn_pressed):
				### if the button has been pressed
				sendGo()
				turnLED_off()
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
	
		if (led_state == 2) and (time.time() - blink_toggle_timer > blink_freq):
			if (blink_toggle):
				GPIO.output(gpio_led_nr, GPIO.LOW)
				blink_toggle = 0
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
