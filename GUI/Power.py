from tkinter import *
from tkinter.ttk import *
from CheckConnect import check_connect
from SendObject import send_obj

def power(s, frame):
  # if check_connect(s) == False: return
  root = frame
  for widget in root.winfo_children():
    widget.destroy()
  root.configure(text='Power')

  Label(root, text='Enter countdown time in seconds :', font='Times 14', anchor=E).place(relx=0.2, rely=0.2, relwidth=0.4, relheight=0.05)
  second = Entry(root, font='Times 14')
  second.place(relx=0.65, rely=0.2, relwidth=0.1, relheight=0.05)

  def shutdown():
    request = ['shutdown', second.get()]
    send_obj(s, request)
    pass

  def logout():
    request = ['logout', second.get()]
    send_obj(s, request)
    pass 

  Button(root, text='Shutdown', command=shutdown).place(relx=0.3, rely=0.6, relwidth=0.15, relheight=0.05)
  Button(root, text='Logout', command=logout).place(relx=0.55, rely=0.6, relwidth=0.15, relheight=0.05)
  