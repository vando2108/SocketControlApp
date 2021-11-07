import json
import sys
import time

def receive_obj(client):
    obj_size = client.recv(8)
    # time.sleep(0.01)
    obj_size = (obj_size.decode("utf8"))
    obj_size = int(obj_size)
    temp = client.recv(obj_size)
    # time.sleep(0.01)
    temp = json.loads(temp.decode())
    return temp['data']

def send_obj(client, obj):
    if not isinstance(obj, dict):
      obj = {"data": obj}
    obj_size = str(len(json.dumps(obj).encode()))
    while len(obj_size) < 8:
      obj_size = '0' + obj_size
    client.sendall(bytes(obj_size, "utf8"))
    # time.sleep(0.01)
    client.sendall(json.dumps(obj).encode())
    # time.sleep(0.01)