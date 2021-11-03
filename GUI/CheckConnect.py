import socket
from tkinter import messagebox
from SendObject import send_obj
import time

def check_connect(s):
    try:
        request = ['check connect']
        send_obj(s, request)
        time.sleep(0.1)
        return True
    except:
        messagebox.showinfo('', 'Not connected to Sever!')
        return False

def time_to_live(s):
    pass
