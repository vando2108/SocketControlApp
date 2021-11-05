from CheckConnect import check_connect
from time import time
from SendObject import send_obj

def logout(s):
  if check_connect(s) == False: return
  request = ['logout']
  send_obj(s, request)
  time.sleep(0.1)
  pass