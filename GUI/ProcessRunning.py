import socket
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from CheckConnect import check_connect
from SendObject import send_obj
from SendObject import receive_obj

list_process = []
lb = None
itemProcess = None

def close_process(s, ID):
    global lb
    request = ['process', 'kill process', ID.get()]
    #for line in lb.get_children():
        #if lb.item(line)['values'][1] == ID.get():
            #lb.delete(line)
    send_obj(s, request)
    mes = receive_obj(s)
    if mes[0] == 'done':
        messagebox.showinfo('', 'Killed process!')
    else: messagebox.showinfo('', "Error!")
    ID.delete(0, END)

def kill_process(s):
    global itemProcess
    close_process(s, str(itemProcess))
    watch_process(s)
    pass

def watch_process(s):
    if check_connect(s) == False: return
    global list_process, lb

    request = ['process', 'watch process']
    send_obj(s, request)
    list_process = receive_obj(s)
    #data = ['1', '2', '3']
    #list_process = [('a', '1', '1'), ('b', '2', '2'), ('c', '7', '3')]
    lb.delete(*lb.get_children())
    for i in range(len(list_process)):
        lb.insert(parent='', index=i, iid=i, text='', values=list_process[i])
    pass

def delete_process():
    global list_process, lb
    list_process.clear()
    lb.delete(*lb.get_children())
    pass

def open_process(s, name_process):
    request = ['process', 'start process', name_process.get()]
    try:
        send_obj(s, request)
        name_process.delete(0, END)
        messagebox.showinfo('', 'Successful open process!')
    except:
        messagebox.showinfo('', 'Opened process!')
    pass

def start_process(s):
    if check_connect(s) == False: return
    root2 = Toplevel()
    root2.grab_set()
    root2.title('Start')
    root2.geometry('300x50')
    name_process = Entry(root2)
    name_process.place(relx=0.05, rely=0.25, relwidth=0.6, relheight=0.5)
    name_process.insert(0, "Enter name's process")
    Button(root2, text = 'Start', command=lambda: open_process(s, name_process)).place(relx=0.7, rely=0.25, relwidth=0.25, relheight=0.5)
    root2.mainloop()
    pass

def selectItem(a):
  global lb, itemProcess
  curItem = lb.focus()
  itemProcess = lb.item(curItem)['values'][1]
  print(itemProcess)
  pass

def process_running(s, frame):
    if check_connect(s) == False: return

    global lb

    root = frame
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(text='Process Running')

    label1 = LabelFrame(root, text='Process Running')
    label1.place(relx=0.04, rely=0.2, relwidth=0.9, relheight=0.7)
    my_scrollbar = Scrollbar(label1, orient=VERTICAL)

    lb = Treeview(label1, yscrollcommand=my_scrollbar.set)
    lb['columns'] = ('Name Process', 'ID Process', 'Count Thread')
    lb.column('#0', width=0, stretch=NO)    
    lb.column('Name Process', width=80, anchor=CENTER)
    lb.column('ID Process', width=80, anchor=CENTER)
    lb.column('Count Thread', width=80, anchor=CENTER)

    lb.heading('#0', text='', anchor=CENTER)
    lb.heading('Name Process', text='Name Process', anchor=CENTER)
    lb.heading('ID Process', text='ID Process', anchor=CENTER)
    lb.heading('Count Thread', text='Count Thread', anchor=CENTER)
    lb.place(relx=0.02, rely=0.02, relwidth=0.92, relheight=0.96)
    lb.bind('<ButtonRelease-1>', selectItem)
    #for x in range(30):
    #    lb.insert(parent='', index=x, iid=x, text='', values=('notepad', x, '2'))

    my_scrollbar.config(command=lb.yview)
    my_scrollbar.place(relx=0.94, rely=0.02, relwidth=0.04, relheight=0.96)

    Button(root, text='Kill', command=lambda: kill_process(s)).place(relx=0.04, rely=0.05, relwidth=0.2, relheight=0.1)
    Button(root, text='Watch', command=lambda: watch_process(s)).place(relx=0.28, rely=0.05, relwidth=0.2, relheight=0.1)
    Button(root, text='Delete', command=lambda: delete_process()).place(relx=0.52, rely=0.05, relwidth=0.2, relheight=0.1)
    Button(root, text='Start', command=lambda: start_process(s)).place(relx=0.76, rely=0.05, relwidth=0.2, relheight=0.1) 
    # root.mainloop()
    pass
