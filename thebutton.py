import websocket
import thread
import time
import json

def on_message(ws, message):
    print message
    msg = json.loads(message)
    print msg["type"]
    if msg["type"] == "registerConfirm": 
		while 1:
			key = raw_input("eingabe bitte: ")
			print key
			ws.send(json.dumps({'type':'playbackAction', 'data':'go'}))

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"
    time.sleep(1)
    open_websocket()

def on_open(ws):
	ws.send(json.dumps({'type':"register", 'data':"go_button"}))

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
    key = input("hit enter")
    print key