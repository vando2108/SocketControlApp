import json

def receive_obj(client):
  temp = client.recv(1024 * 2)
  temp = json.loads(temp.decode())  
  return temp

def send_obj(client, obj):
  client.sendall(json.dumps(obj).encode())