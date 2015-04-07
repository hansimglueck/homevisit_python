#!/usr/bin/env python
#from time import sleep
import time
import os
import RPi.GPIO as GPIO
import ws
import sys

GPIO.setmode(GPIO.BCM)
	
#def initParams():
gpio_nr = 23
sending_param = "0"
gpio_led_nr = 17
instance_name = "gruen"

btn_pressed = 0

print("Setze alle Parameter auf Anfang")
led_state = None
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


#initParams()
try:

	GPIO.setup(23, GPIO.IN)
	GPIO.setup(17, GPIO.OUT)
	led_state = 0

except:
	print("GPIO already in use")
	led_state = 0
	
else:
	led_state = 0
	
	def sendGo():
		print("GO GO GO")
	
	def sendShutDown():
		print("System ausschalten!")
		#p.print_text("G O N N A * S L E E P * N O W\n")
		#p.print_text("* * * * * * B Y E * * * * * *\n")
		#p.print_text("-----------------------------\n")
	
	def cb(msg):
		global led_state
		if (msg == "button_led"):
			cmd = "alarm"
			print(cmd)
			if (cmd == "on"):
				turnLED_on()
			elif (cmd == "off"):
				turnLED_off()
			elif (cmd == "blink"):
				blink(msg["data"]["param"])
			elif (cmd == "alarm"):
				if (led_state == 0):
					turnLED_on()
					led_state = 1
					#blink(msg["data"]["param"])
				elif (led_state == 1):
					blink(1)
					led_state = 2
				elif (led_state == 2):
					turnLED_off()
					led_state = 0
		print("button cb got message")
				
		
	def turnLED_off():
		print("LED OFF")
		
		print(led_state)
		GPIO.output(gpio_led_nr, GPIO.LOW)
		blink_toggle = 0
		
	def turnLED_on():
		print("LED ON")
		
		print(led_state)
		GPIO.output(gpio_led_nr, GPIO.HIGH)
		blink_toggle = 0
		
	def blink(freq):
		print("LED BLINK")
		
		print(led_state)
		blink_freq = freq
		if (blink_freq == 0):
			blink_freq = 1.5
		GPIO.output(gpio_led_nr, GPIO.HIGH)
		blink_toggle = 1
		blink_toggle_timer = time.time()

	while not stop_proc:
		print(led_state)
		if ( GPIO.input(gpio_nr) == False):
			if (not btn_pressed):
				### if the button has been pressed
				sendGo()
				cb("button_led")
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
				GPIO.output(gpio_led_nr, GPIO.LOW)
				blink_toggle = 0
				blink_toggle_timer = time.time()
			else:
				GPIO.output(gpio_led_nr, GPIO.HIGH)
				blink_toggle = 1
				blink_toggle_timer = time.time()				
		time.sleep(0.1);
	
	if (stop_proc):
		sendShutDown()
		### shutdown system

finally:
	GPIO.cleanup()
