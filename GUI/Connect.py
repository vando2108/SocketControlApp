import socket
from tkinter import messagebox

def connect(s, HOST, PORT):
    try:
        s.connect((HOST, PORT))
        messagebox.showinfo('', 'Connect successfully')
        return
    except:
        messagebox.showinfo('', 'Error connecting to Sever.')
    pass

'''from tkinter import * 

win = Tk()
win.geometry('400x400')

def alo(root):
    root2 = Toplevel(root)
    root2.title('nge')
    root2.geometry('222x222')
    root2.transient(root)
    root2.grab_set()
    #root2.mainloop()
    pass

def but():
    root = Toplevel(win)
    root.title('root')
    root.geometry('300x300+100+100')
    Button(root, text='Alo', command=lambda: alo(root)).pack()
    root.transient(win)
    root.grab_set()
    #root.mainloop()
    pass

Button(win, text='Ok', command=but).pack()
win.mainloop()'''