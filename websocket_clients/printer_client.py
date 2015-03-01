#!/usr/bin/env python
#coding=utf-8

import time
import json
import printer_gs, textwrap
import ws
import logging
logging.basicConfig(filename='printer_client.log',level=logging.DEBUG)

p=printer_gs.ThermalPrinter(serialport="/dev/ttyAMA0")

def printChunkDoubleSize(txt):
	unicode = txt.encode('utf-8')
	#if (txt.startswith('***PICTURE***')):
		#lineBreaksNum = txt.count('\n')
		#picTag = txt.splitlines(lineBreaksNum)[0]
		#picFileName = txt.splitlines(lineBreaksNum)[1]
		#p.print_from_file(picFileName.strip("\n"))
		#txt = txt.replace(picTag,"")
		#txt = txt.replace(picFileName,"")
	lines = unicode.splitlines(txt.count('\n'))

	if (lines[0] == "***PICTURE***\n"):
		p.print_from_file(lines[1].strip("\n"))
		lines.pop(0)
		lines.pop(0)
	#p.print_text("\x84")
	p.double_width(True)
	p.set_linespacing(35)
	for item in lines:
                #print item
		item = replaceSpecialChars(item)
                unwrapped = item
                wrapped = textwrap.fill(unwrapped, 16)
		#logging.info("printing: "+wrapped)
                p.print_text(wrapped)
                p.print_text("\n")
	#unwrapped = txt
	#wrapped = textwrap.fill(unwrapped, 16)
	#p.print_text(wrapped)
	#p.print_text("\n")
	p.double_width(False)
	p.reset_linespacing()
	p.print_text("\n\n\n\n\n\n\n")
	p.print_text("--------------------------------\n")
	p.print_text("\n\n")
	p.linefeed()
	p.linefeed()

def replaceSpecialChars(txt):
        specialChars = {'Ä':'\x8E', 'ä':'\x84', 'Ö':'\x99', 'ö':'\x94', 'Ü':'\x9A', 'ü':'\x81', 'ß':'\xE1'}
        for i, j in specialChars.iteritems():
                txt = txt.replace(i, j)
        return txt

def test(x):
	print x

#der client wird in einem extra-thread gestartet...
client = ws.Client(role="printer", cb = printChunkDoubleSize)


#damit das programm nicht stoppt
#c = raw_input("Client running.")
while True:
	time.sleep(1)
