import json
import sys

from numpy.lib.arraysetops import isin

def receive_obj(client):
	obj_size = client.recv(8)
	obj_size = int(obj_size.decode("utf8"))
	temp = client.recv(obj_size)
	temp = json.loads(temp.decode('utf8'))
	return temp['data']

def send_obj(client, obj):
	if not isinstance(obj, dict):
		obj = {"data": obj}
	obj_size = str(sys.getsizeof(obj))
	while len(obj_size) < 8:
		obj_size = '0' + obj_size
	client.sendall(bytes(obj_size, "utf8"))
	print(obj)
	client.sendall(json.dumps(obj).encode())