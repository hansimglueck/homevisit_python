import ws
import time

def test(content):
	print content

#der client wird in einem extra-thread gestartet...
#das programm darf nicht auslaufen, deswegen am ende raw_input()	
client = ws.Client(role="hallo", cb = test)

#eigentlich muesste irgendwie klargemacht werden, wann die websocket-connection besteht
#erst dann kann auch was gesendet werden
#hier wird erstmal eine sekunde gewartet ;)
time.sleep(1)

client.send(type="playbackAction", data="go")

#damit das programm nicht stoppt
c = raw_input("Client running.")