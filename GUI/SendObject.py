import json
import sys

from numpy.lib.arraysetops import isin

def receive_obj(client):
	obj_size = client.recv(8)
	obj_size = (obj_size.decode("utf8"))
	print(obj_size)
	obj_size = int(obj_size)
	temp = client.recv(obj_size)
	print(temp)
	temp = json.loads(temp.decode())
	return temp['data']

def send_obj(client, obj):
	if not isinstance(obj, dict):
		obj = {"data": obj}
	obj_size = str(sys.getsizeof(json.dumps(obj).encode()))
	print(obj_size)
	print(obj)
	while len(obj_size) < 8:
		obj_size = '0' + obj_size
	client.sendall(bytes(obj_size, "utf8"))
	client.sendall(json.dumps(obj).encode())

def receive_image(client):
	obj_size = client.recv(8)
	obj_size = int(obj_size.decode())
	data = client.recv(obj_size)
	return data