from tkinter import *
from tkinter.ttk import *
import socket
import Connect, FileExplorer, MACAddress, ProcessRunning, AppRunning, ShutDown
import LiveScreen
import KeyStroke, Logout, Screenshot
from CheckConnect import check_connect
from SendObject import send_obj

HOST = '127.0.0.1'
PORT = 9090

def quit_button(s, win):
    if check_connect(s):
        send_obj(s, ["quit"])
        s.close()
    win.destroy()
    pass

if __name__ == '__main__':
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    win = Tk()
    win.title('Client')
    win.geometry('1000x650+100+20')
    IP = Entry(win, font='Times 14')
    IP.place(relx=0.05, rely=0.05, relwidth=0.6, relheight=0.1)
    IP.insert(0, '127.0.0.1')
    Button(win, text='Connect', command=lambda: Connect.connect(
        s, IP.get(), PORT)).place(relx=0.67, rely=0.05, relwidth=0.28, relheight=0.1)
    Button(win, text='Process\nRunning', command=lambda: ProcessRunning.process_running(
        s)).place(relx=0.05, rely=0.18, relwidth=0.18, relheight=0.47)
    Button(win, text='MAC\nAddress', command=lambda: MACAddress.MAC_address(
        s)).place(relx=0.05, rely=0.67, relwidth=0.18, relheight=0.21)
    Button(win, text='App Running', command=lambda: AppRunning.application_running(
        s)).place(relx=0.25, rely=0.18, relwidth=0.4, relheight=0.2)
    Button(win, text='Shut down', command=lambda: ShutDown.shut_down(
        s)).place(relx=0.25, rely=0.4, relwidth=0.19, relheight=0.25)
    Button(win, text='Logout', command=lambda: Logout.logout(
        s)).place(relx=0.46, rely=0.4, relwidth=0.19, relheight=0.25)
    Button(win, text='Key\nStroke', command=lambda: KeyStroke.key_stroke(
        s)).place(relx=0.67, rely=0.18, relwidth=0.28, relheight=0.2)
    # Button(win, text='Live\nScreen', command=lambda: Screenshot.screenshot(
    #     s)).place(relx=0.67, rely=0.4, relwidth=0.28, relheight=0.25)
    Button(win, text='Live\nScreen', command=lambda: LiveScreen.live_screen(
        s)).place(relx=0.67, rely=0.4, relwidth=0.28, relheight=0.25)
    Button(win, text='File Explorer', command=lambda: FileExplorer.file_explorer(
        s)).place(relx=0.25, rely=0.67, relwidth=0.48, relheight=0.21)
    Button(win, text='Quit', command=lambda: quit_button(s, win)).place(
        relx=0.75, rely=0.67, relwidth=0.2, relheight=0.21)
        
    win.mainloop()
    s.close()
