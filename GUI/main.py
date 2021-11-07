from tkinter import *
from tkinter.ttk import *
import socket
import Connect, FileExplorer, MACAddress, ProcessRunning, AppRunning
import LiveScreen
import KeyStroke, Power, EditRegistry
from CheckConnect import check_connect
from SendObject import send_obj

HOST = '127.0.0.1'
PORT = 9090

def quit_button(s):
    if check_connect(s):
        send_obj(s, ["quit"])
        s.close()
    pass

if __name__ == '__main__':
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    win = Tk()
    win.title('Client')
    win.geometry('1000x650+100+20')

    # Frame 1
    frame1 = LabelFrame(win, text='Connecting')
    frame1.place(relx=0.02, rely=0.01, relwidth=0.9, relheight=0.08)
    Label(frame1, text='IP Address :', anchor=E).place(relx=0.02, rely=0.02, relwidth=0.15, relheight=0.9)
    IP = Entry(frame1, font='Times 14')
    IP.place(relx=0.2, rely=0.02, relwidth=0.4, relheight=0.9)
    IP.insert(0, '127.0.0.1')
    Button(frame1, text='Connect', command=lambda: Connect.connect(
        s, IP.get(), PORT)).place(relx=0.65, rely=0.02, relwidth=0.1, relheight=0.9)
    Button(frame1, text='Disconnect', command=lambda: quit_button(
        s)).place(relx=0.8, rely=0.02, relwidth=0.1, relheight=0.9)
    
    # Frame 2
    frame2 = LabelFrame(win, text='Services')
    frame2.place(relx=0.02, rely=0.1, relwidth=0.15, relheight=0.87)

    # Frame 3
    frame3 = LabelFrame(win, text = '')
    frame3.place(relx=0.2, rely=0.1, relwidth=0.77, relheight=0.87)
    frame3.configure(text='Show')

    # services
    process = Button(frame2, text='Process Running', command=lambda: ProcessRunning.process_running(s, frame3))
    app = Button(frame2, text='App Running', command=lambda: AppRunning.application_running(s, frame3))
    mac = Button(frame2, text='MAC Address', command=lambda: MACAddress.MAC_address(s, frame3))
    key = Button(frame2, text='Key Stroke', command=lambda: KeyStroke.key_stroke(s, frame3))
    registry = Button(frame2, text='Registry', command=lambda: EditRegistry.edit_registry(s, frame3))
    live = Button(frame2, text='Live Screen', command=lambda: LiveScreen.live_screen(s, frame3))
    folder = Button(frame2, text='Tree Folder', command=lambda: FileExplorer.file_explorer(s, frame3))
    sys = Button(frame2, text='Shutdown/Logout ', command=lambda: Power.power(s, frame3))

    list = [process, app, mac, key, registry, live, folder, sys]
    for i in range(len(list)):
      list[i].place(relx=0, rely=i/len(list), relwidth=1, relheight=1/len(list))
        
    win.mainloop()
    s.close()
