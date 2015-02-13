#from time import sleep
import time
import os
import RPi.GPIO as GPIO
import ws

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)

btn_pressed = 0

# for shutting down the system by holding the white button longer than 5 seconds
stop_timer = time.time()
stop_timer_hold = 0
stop_proc = 0

def sendGo():
	print("GO GO GO")
	client.send(type="playbackAction", data="go")

def sendShutDown():
	print("System ausschalten!")
        #p.print_text("G O N N A * S L E E P * N O W\n")
        #p.print_text("* * * * * * B Y E * * * * * *\n")
        #p.print_text("-----------------------------\n")

#der client wird in einem extra-thread gestartet...
client = ws.Client(role="button")


while not stop_proc:
        if ( GPIO.input(23) == False):
		if (not btn_pressed):
			### if the button has been pressed
			sendGo()
                        stop_timer = time.time()
                        stop_timer_hold = 0
                        btn_pressed = 1
                else:
			### if the button is being pressed down longer
                        #print(stop_timer_hold)
                        stop_timer_hold = time.time() - stop_timer
                        if (stop_timer_hold > 5 and not stop_proc):
                                stop_proc = 1
        if (GPIO.input(23) == True):
		### button is not pressed
                btn_pressed = 0

        time.sleep(0.1);

if (stop_proc):
        sendShutDown()
        ### shutdown system
        command = "/usr/bin/sudo /sbin/shutdown -h now"
        import subprocess
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output

