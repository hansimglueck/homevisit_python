import time
import json
import printer_gs, textwrap
import ws

p=printer_gs.ThermalPrinter(serialport="/dev/ttyAMA0")

def printChunkDoubleSize(ch):
	p.double_width(True)
	#p.double_height(True)
	p.set_linespacing(35)
	#print item
	unwrapped = ch
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

#der client wird in einem extra-thread gestartet...
client = ws.Client(role="button", cb = printChunkDoubleSize)



