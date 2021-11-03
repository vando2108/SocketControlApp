import socket
from tkinter import messagebox
from SendObject import send_obj

def shut_down(s):
    request = ['Shutdow']
    send_obj(s, request)
    pass