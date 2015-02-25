import websocket
import thread
import time
import json
import logging

class Client(object):
	
	def __init__(self, role, cb):
		logging.info("Client:init")
		self.connected = False
		self.cb = cb
		self.role = role
		websocket.enableTrace(True)
		self.open_websocket()
		
	def on_message(self, ws, message):
		#print message
		msg = json.loads(message)
		#print msg["type"]
		if msg["type"] == "registerConfirm": logging.info("registered at the game")
		if msg["type"] == "display":
			#print msg["data"]["text"]
			self.cb(msg["data"]["text"])
	
	def on_error(self, ws, error):
	    print error

	def on_close(self, ws):
		logging.info("Socket closed")
		self.connected = False
		print "### closed ###"
		time.sleep(1)
		self.open_websocket()

	def on_open(self, ws):
		logging.info("Socket opened")
		self.connected = True
		self.ws.send(json.dumps({'type':"register", 'data':self.role}))
		
	def open_websocket(self):
		def run(* args):
			self.ws = websocket.WebSocketApp("ws://localhost:80",
		                          on_message = self.on_message,
		                          on_error = self.on_error,
		                          on_close = self.on_close)
			self.ws.on_open = self.on_open
			self.ws.run_forever()
			print "konnte keine verbindung aufbauen"
		thread.start_new_thread(run, ())

	def send(self, type, data, param):
		print "send send"
		self.ws.send(json.dumps({'type':type, 'data':data, 'param':param}))

	def conn(self):
		return self.connected
