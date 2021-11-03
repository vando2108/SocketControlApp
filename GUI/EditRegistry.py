from os import name
import socket
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
from CheckConnect import check_connect
from SendObject import send_obj, receive_obj

root, sf, path, t = None, None, None, None
namee, valuee, typee = None, None, None
select_path, text_2 = None, None
list_type = ['String', 'Binary', 'DWORD', 'QWORD', 'Multi-String', 'Expandable String']

def browserFiles():
    global path, t
    filename = filedialog.askopenfilename(initialdir='/', title='Select a File', filetypes=(("Text files", "*.txt*"), ("all files", "*.*")))
    path.delete(0, END)
    path.insert(END, filename)
    filename = open(filename)
    data = filename.read()
    t.delete('1.0', END)
    t.insert(END, data)
    pass

def send_content(s):
    if check_connect(s) == False: return
    global t
    request = ['registry', 'send file', t.get('1.0', END)]
    send_obj(s, request)
    pass

def function_changed(event):    
    global root, sf, namee, valuee, typee
    func = sf.get()
    if func == 'Get value':
        namee.place(relx=0.05, rely=0.49, relwidth=0.28, relheight=0.05)
        valuee.place_forget()
        typee.place_forget()
        pass
    if func == 'Set value': 
        namee.place(relx=0.05, rely=0.49, relwidth=0.28, relheight=0.05)
        valuee.place(relx=0.35, rely=0.49, relwidth=0.28, relheight=0.05)
        typee.place(relx=0.65, rely=0.49, relwidth=0.3, relheight=0.05)
        pass
    if func == 'Delete value':
        namee.place(relx=0.05, rely=0.49, relwidth=0.28, relheight=0.05)
        valuee.place_forget()
        typee.place_forget()
        pass
    if func == 'Create key':
        namee.place_forget()
        valuee.place_forget()
        typee.place_forget()
        pass
    if func == 'Delete key':
        namee.place_forget()
        valuee.place_forget()
        typee.place_forget()
        pass

def Send(s):
    if check_connect(s) == False: return
    global select_path, sf, namee, valuee, typee, text_2, list_type

    data = ['registry', sf.get(), select_path.get(), namee.get(), valuee.get(), typee.get()]
    send_obj(s, data)
    mess = receive_obj(s)
    text_2.configure(state=NORMAL)
    text_2.insert(END, mess)
    text_2.insert(END, '\n')
    text_2.configure(state='disabled')
    pass

def Delete():
    global text_2
    text_2.configure(state=NORMAL)
    text_2.delete('1.0', END)
    text_2.configure(state='disabled')
    pass

def edit_registry(s):
    if check_connect(s) == False: return
    global root, path, t, sf, namee, valuee, typee, select_path, text_2

    root = Toplevel()
    root.grab_set()
    root.title("registry")
    root.geometry("500x500+100+100")
    path = Entry(root, font = 'Times 10')
    path.insert(END, "Path")
    path.place(relx=0.05, rely=0.02, relwidth=0.65, relheight=0.05)
    my_scrollbar = Scrollbar(root, orient=VERTICAL)
    t = Text(root, yscrollcommand=my_scrollbar.set)
    t.place(relx=0.05, rely=0.09, relwidth=0.62, relheight=0.25)
    my_scrollbar.config(command=t.yview)
    my_scrollbar.place(relx=0.67, rely=0.09, relwidth=0.03, relheight=0.25)
    Button(root, text='Browser..', command= browserFiles).place(relx=0.75, rely=0.02, relwidth=0.2, relheight=0.05)
    Button(root, text='Send content', command= lambda: send_content(s)).place(relx=0.75, rely=0.09, relwidth=0.2, relheight=0.25)
    
    Label(root, text='Direct edit value').place(relx=0.05, rely=0.35)
    sf = Combobox(root)
    sf.place(relx=0.05, rely=0.36, relwidth=0.9, relheight=0.05)

    sf['values'] = ('Select function', 'Get value', 'Set value', 'Delete value', 'Create key', 'Delete key')
    sf.current(0)
    sf['values'] = ('Get value', 'Set value', 'Delete value', 'Create key', 'Delete key')
    sf.bind('<<ComboboxSelected>>', function_changed)

    namee = Entry(root, font='Times 10')
    namee.place(relx=0.05, rely=0.49, relwidth=0.28, relheight=0.05)
    namee.insert(END, 'Value Name')

    valuee = Entry(root, font='Times 10')
    valuee.place(relx=0.35, rely=0.49, relwidth=0.28, relheight=0.05)
    valuee.insert(END, 'Name')

    typee = Combobox(root)
    typee.place(relx=0.65, rely=0.49, relwidth=0.3, relheight=0.05)
    typee['values'] = ('Data type', '2')
    typee.current(0)
    typee['values'] = ('String', 'Binary', 'DWORD', 'QWORD', 'Multi-String', 'Expandable String')
    
    select_path = Entry(root, font='Times 10')
    select_path.place(relx=0.05, rely=0.42, relwidth=0.9, relheight=0.05)
    select_path.insert(END, 'Enter key path')

    text_2 = Text(root)
    text_2.place(relx=0.05, rely=0.56, relwidth=0.9, relheight=0.3)
    text_2.configure(state='disabled')
    Button(root, text='Send', command=lambda: Send(s)).place(relx=0.2, rely=0.90, relwidth=0.2, relheight=0.05)
    Button(root, text='Delete', command=Delete).place(relx=0.5, rely=0.90, relwidth=0.2, relheight=0.05)

    root.mainloop()
    pass