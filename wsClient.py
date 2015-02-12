import ws


def test(content):
	print content
	
client = ws.Client(role="hallo", cb = test)
