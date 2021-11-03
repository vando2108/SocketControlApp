import socket
import pickle
from struct import *

def send_obj(client, obj):
    msg = pickle.dumps(obj)
    length = pack('>Q',len(msg))
    client.sendall(length)
    client.sendall(msg)

def receive_obj(client):
	msg = bytearray()
	header = client.recv(4096)
	(length,) = unpack('>Q',header)
	length_recv = 0
	while length_recv < length:
		s = client.recv(4096)
		msg += s
		length_recv += len(s)
	return pickle.loads(msg)

'''def send_obj(client, obj):
    for x in obj:
        client.sendall(bytes(x, 'utf8'))

def receive_obj(client):
	client.recv(1024).decode('utf8')'''