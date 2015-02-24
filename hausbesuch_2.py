#from time import sleep
import time
import os
import RPi.GPIO as GPIO
import printer_gs, textwrap

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)

white_pressed = 0

testcounter = 0

# for shutting down the system by holding the white button longer than 5 seconds
stop_timer = time.time()
stop_timer_hold = 0
stop_proc = 0

# for music playing
music = 0

# save my process ID
procID = os.getpid()

# Welcome print  --- raspi is up, program is running #
p=printer_gs.ThermalPrinter(serialport="/dev/ttyAMA0")
p.print_text("* * * * W E L C O M E * * * *\n")
p.print_text("-----------------------------\n")
p.print_text("My Proc-ID is: ")
p.print_text(str(procID))
p.print_text("\n")

### This is for saving img data into a file
#i = Image.open("wiener_kongress_1bit.png")
#data = list(i.getdata())
#w, h = i.size
#p.print_bitmap(data, w, h, True)

### This is for fast printing images from prepared pixel data files
#p.print_from_file('europa_black_data')
#p.print_from_file('europa_kontur_data')

p.print_text("\n\n\n")
p.linefeed()
p.linefeed()
p.linefeed()

def getChunk(f):
	myList = []
	insideChunk = True
	while (insideChunk):
		line = f.readline()
		if (line == "\n"):
			insideChunk = False
		else:
			myList.append(line)
	return myList

def printChunk(ch):
	#p.set_linespacing(40)
	for item in ch:
	        #print item
		unwrapped = item
		wrapped = textwrap.fill(unwrapped, 32)
		p.print_text(wrapped)
		p.print_text("\n")
	#p.reset_linespacing()
	p.print_text("\n\n\n\n\n\n\n")
	p.print_text("--------------------------------\n")
	p.print_text("\n\n")
	p.linefeed()
	p.linefeed()
	#os.system("/usr/games/fortune -s science | python printer_04.py")

def printChunkDoubleSize(ch):
	p.double_width(True)
	#p.double_height(True)
        p.set_linespacing(35)
	for item in ch:
                #print item
                unwrapped = item
                wrapped = textwrap.fill(unwrapped, 16)
                p.print_text(wrapped)
                p.print_text("\n")
	p.double_width(False)
	#p.double_height(False)
	p.reset_linespacing()
	p.print_text("\n\n\n\n\n\n\n")
        p.print_text("--------------------------------\n")
        p.print_text("\n\n")
        p.linefeed()
        p.linefeed()

def printChunkTiny(ch):
	p.font_b_on()
        p.set_linespacing(15)
        for item in ch:
                #print item
                unwrapped = item
                wrapped = textwrap.fill(unwrapped, 42)
                p.print_text(wrapped)
                p.print_text("\n")
        p.font_b_off()
	p.reset_linespacing()
	p.linefeed()
        p.linefeed()

def sendGo():
	print("GO GO GO")

textfile = open("print_02_12.txt", "r")

while not stop_proc:
        if ( GPIO.input(23) == False):
                if (not white_pressed):
			sendGo()
			if (music):
				#print("Musik beenden")
				#os.system('pkill mpg321')
				os.system('sudo sh pifmplay/pifmplay stop')
				music = 0
			chunk = getChunk(textfile)
			if (chunk[0] == "***ENDE***"):
				p.print_text("* * * * T H E * E N D * * * *\n")
				p.print_text("--------------------------------\n")
				stop_proc = 1
				#textfile.close()
				#textfile = open("print_01_27.txt", "r")
			elif (chunk[0] == "***SOUND***\n"):
				#os.system('mpg321 ' + chunk[1].strip("\n") + ' &')
                                #music = os.popen('mpg321 ' + chunk[1].strip("\n") + ' &')
				#print('sudo sh pifmplay/pifmplay ' + chunk[1].strip("\n") + ' 100.5 &>/dev/null &')
				os.system('sudo sh pifmplay/pifmplay ' + chunk[1].strip("\n") + ' 100.5 &>/dev/null &')
				music = 1
				if (len(chunk) > 2):
                                        chunk.pop(0)
                                        chunk.pop(0)
                                        #printChunk(chunk)
                                        #printChunkTiny(chunk)
					printChunkDoubleSize(chunk)
				#os.system('mpg321 white.mp3 &')
			elif (chunk[0] == "***PICTURE***\n"):
				p.print_text("--------------------------------\n")
				p.print_from_file(chunk[1].strip("\n"))
				if (len(chunk) > 2):
					chunk.pop(0)
					chunk.pop(0)
					#printChunk(chunk)
					#printChunkTiny(chunk)
					printChunkDoubleSize(chunk)
			else:
				p.print_text("--------------------------------\n")
				printChunkDoubleSize(chunk)
				#printChunkTiny(chunk)
				#printChunk(chunk)
                        stop_timer = time.time()
                        stop_timer_hold = 0
                        white_pressed = 1
                else:
                        #print(stop_timer_hold)
                        stop_timer_hold = time.time() - stop_timer
                        if (stop_timer_hold > 5 and not stop_proc):
                                stop_proc = 1
        if (GPIO.input(23) == True):
                white_pressed = 0

        time.sleep(0.1);

if (stop_proc):
        #print("System ausschalten!")
        textfile.close()
	p.print_text("G O N N A * S L E E P * N O W\n")
        p.print_text("* * * * * * B Y E * * * * * *\n")
        p.print_text("-----------------------------\n")
        # shutdown system
        p.print_text("\n\n\n")
        command = "/usr/bin/sudo /sbin/shutdown -h now"
        import subprocess
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output

