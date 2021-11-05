import socket
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from CheckConnect import check_connect
from SendObject import send_obj
from SendObject import receive_obj

list_application = []
lb = None
itemApp = None

def close_application(s, ID):
    global lb
    request = ['application', 'kill application', ID]
    send_obj(s, request)
    mes = receive_obj(s)
    if mes[0] == 'done':
        messagebox.showinfo('', 'Killed application!')
    else: messagebox.showinfo('', "Error!")

def kill_application(s):
    global itemApp
    close_application(s, str(itemApp))
    watch_application(s)
    pass

def receivedListapplication(s):
    global list_application
    list_application.clear()
    while True:
        data = receive_obj(s)
        if data[0] == 'done':
            break
        list_application.append(data)
    #return list_application
    pass

def watch_application(s):
    #if check_connect(s) == False: return
    global list_application, lb

    request = ['application', 'watch application']
    send_obj(s, request)
    receivedListapplication(s)
    #data = ['1', '2', '3']
    #list_application = [('a', '1', '1'), ('b', '2', '2'), ('c', '7', '3')]
    lb.delete(*lb.get_children())
    for i in range(len(list_application)):
        lb.insert(parent='', index=i, iid=i, text='', values=list_application[i])
    pass

def delete_application():
    global list_application, lb
    list_application.clear()
    lb.delete(*lb.get_children())
    pass

def open_application(s, name_application):
    request = ['application', 'start application', name_application.get()]
    try:
        send_obj(s, request)
        name_application.delete(0, END)
        messagebox.showinfo('', 'Successful open application!')
    except:
        messagebox.showinfo('', 'Opened application!')
    pass

def start_application(s):
    if check_connect(s) == False: return
    root2 = Toplevel()
    root2.grab_set()
    root2.title('Start')
    root2.geometry('300x50')
    name_application = Entry(root2)
    name_application.place(relx=0.05, rely=0.25, relwidth=0.6, relheight=0.5)
    name_application.insert(0, "Enter name's application")
    Button(root2, text = 'Start', command=lambda: open_application(s, name_application)).place(relx=0.7, rely=0.25, relwidth=0.25, relheight=0.5)
    root2.mainloop()
    pass

def selectItem(a):
  global lb, itemApp
  curItem = lb.focus()
  itemApp = lb.item(curItem)['values'][1]
  print(itemApp)
  pass

def application_running(s):
    if check_connect(s) == False: return

    global lb

    root = Toplevel()
    root.grab_set()
    root.title('application')
    root.geometry('400x400')
    
    label1 = LabelFrame(root, text='App Running')
    label1.place(relx=0.04, rely=0.2, relwidth=0.9, relheight=0.7)
    my_scrollbar = Scrollbar(label1, orient=VERTICAL)

    lb = Treeview(label1, yscrollcommand=my_scrollbar.set)
    lb['columns'] = ('Name application', 'ID application', 'Count Thread')
    lb.column('#0', width=0, stretch=NO)    
    lb.column('Name application', width=80, anchor=CENTER)
    lb.column('ID application', width=80, anchor=CENTER)
    lb.column('Count Thread', width=80, anchor=CENTER)

    lb.heading('#0', text='', anchor=CENTER)
    lb.heading('Name application', text='Name application', anchor=CENTER)
    lb.heading('ID application', text='ID application', anchor=CENTER)
    lb.heading('Count Thread', text='Count Thread', anchor=CENTER)
    lb.place(relx=0.02, rely=0.02, relwidth=0.92, relheight=0.96)
    lb.bind('<ButtonRelease-1>', selectItem)
    #for x in range(30):
    #    lb.insert(parent='', index=x, iid=x, text='', values=('notepad', x, '2'))

    my_scrollbar.config(command=lb.yview)
    my_scrollbar.place(relx=0.94, rely=0.02, relwidth=0.04, relheight=0.96)

    Button(root, text='Kill', command=lambda: kill_application(s)).place(relx=0.04, rely=0.05, relwidth=0.2, relheight=0.1)
    Button(root, text='Watch', command=lambda: watch_application(s)).place(relx=0.28, rely=0.05, relwidth=0.2, relheight=0.1)
    Button(root, text='Delete', command=lambda: delete_application()).place(relx=0.52, rely=0.05, relwidth=0.2, relheight=0.1)
    Button(root, text='Start', command=lambda: start_application(s)).place(relx=0.76, rely=0.05, relwidth=0.2, relheight=0.1) 
    root.mainloop()
    pass
