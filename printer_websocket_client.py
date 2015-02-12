import websocket
import thread
import time
import json
import printer_gs, textwrap

p=printer_gs.ThermalPrinter(serialport="/dev/ttyAMA0")

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

def on_message(ws, message):
    msg = json.loads(message)
    #print msg["type"]
    print ""
    if msg["type"] == "registerConfirm": print "registered at the game"
    if msg["type"] == "display":
        print msg["data"]["text"]
        p.print_text("--------------------------------\n")
        printChunkDoubleSize(msg["data"]["text"])


def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"
    time.sleep(1)
    open_websocket()

def on_open(ws):
	ws.send(json.dumps({'type':"register", 'data':"printer"}))

def open_websocket():
    ws = websocket.WebSocketApp("ws://localhost:3000",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    websocket.enableTrace(True)
    open_websocket()