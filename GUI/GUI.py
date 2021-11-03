from tkinter import *
from tkinter.ttk import *
import socket
import Connect, ProcessRunning, AppRunning, ShutDown, Screenshot, KeyStroke, EditRegistry
from SendObject import send_obj

win = Tk()
win.title('Client')
win.geometry('500x400')

HOST = '127.0.0.1'
PORT = 9090

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((HOST, PORT))

def quit_button():
    try:
        send_obj(s, ['check_connect'])
        s.close()
        return
    except:
        pass
    win.destroy()
    pass

IP = Entry(win, font='Times 14')
IP.place(relx=0.05, rely=0.05, relwidth=0.6, relheight=0.1)
IP.insert(0, 'Enter IP Address')
Button(win, text='Connect', command=lambda: Connect.connect(s, IP.get(), PORT)).place(relx=0.67, rely=0.05, relwidth=0.28, relheight=0.1)
Button(win, text='Process\nRunning', command=lambda: ProcessRunning.process_running(s)).place(relx=0.05, rely=0.18, relwidth=0.18, relheight=0.7)
Button(win, text='App Running',command=lambda: AppRunning.application_running(s)).place(relx=0.25, rely=0.18, relwidth=0.4, relheight=0.2)
Button(win, text='Shut\ndown',command=lambda: ShutDown.shut_down(s)).place(relx=0.25, rely=0.4, relwidth=0.13, relheight=0.25)
Button(win, text='Screenshot',command=lambda: Screenshot.screenshot(s)).place(relx=0.4, rely=0.4, relwidth=0.25, relheight=0.25)
Button(win, text='Key\nStroke', command=lambda: KeyStroke.key_stroke(s)).place(relx=0.67, rely=0.18, relwidth=0.28, relheight=0.47)
Button(win, text='Fix Registry', command=lambda: EditRegistry.edit_registry(s)).place(relx=0.25, rely=0.67, relwidth=0.48, relheight=0.21)
Button(win, text='Quit', command=quit_button).place(relx=0.75, rely=0.67, relwidth=0.2, relheight=0.21)
win.mainloop()
s.close()