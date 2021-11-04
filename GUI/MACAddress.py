from time import time
from tkinter import *
from tkinter.ttk import *
from CheckConnect import check_connect
from SendObject import receive_obj, send_obj


def MAC_address(s):
  # if check_connect(s) == False: return
  # request = ['mac address']
  # send_obj(s, request)
  # time.sleep(0.1)
  # response = receive_obj(s)
  
  root = Toplevel()
  root.grab_set
  root.title('MAC Address')
  root.geometry('500x500+100+100')
  my_scrollbar = Scrollbar(root, orient=VERTICAL)
  t = Text(root, yscrollcommand=my_scrollbar.set)
  t.place(relx=0.05, rely=0.05, relwidth=0.86, relheight=0.9)
  t.insert(END, 'mac address')

  my_scrollbar.config(command=t.yview)
  my_scrollbar.place(relx=0.91, rely=0.05, relwidth=0.04, relheight=0.9)


  
  
