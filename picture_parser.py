import os
import printer_gs, textwrap
import Image, ImageDraw

### This is for saving img data into a file
def parsePictureFile(filename):
	p=printer_gs.ThermalPrinter(serialport="/dev/ttyAMA0")
	i = Image.open(filename)
	data = list(i.getdata())
	w, h = i.size

    	newfilename = filename[:-4] + "_data"
	print("Create " + newfilename)
	p.print_bitmap(data, w, h, newfilename, True)


### This is for fast printing images from prepared pixel data files
def printFromDataFile(filename):
	p=printer_gs.ThermalPrinter(serialport="/dev/ttyAMA0")
	p.print_from_file(filename)
	p.print_text("\n\n\n")
	p.linefeed()
	p.linefeed()
	p.linefeed()
