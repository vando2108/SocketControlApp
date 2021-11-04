from time import time
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from CheckConnect import check_connect
from SendObject import receive_obj, send_obj

path = None
lfolder, lfile = None, None
itemFolder, itemFile = None, None 
pathList = ["C"]

def selectItemFolder(a):
  global itemFolder, lfolder
  print(type(lfolder))
  curItem = lfolder.focus()
  itemFolder = lfolder.item(curItem)['values'][0]
  print(itemFolder)
  pass

def selectItemFile(a):
  global itemFile, lfile
  print(type(lfile))
  curItem = lfile.focus()
  itemFile = lfile.item(curItem)['values'][0]
  print(itemFile)
  pass

def requestPath(s, request):
  send_obj(s, request)
  time.sleep(0.1)
  listFolder = receive_obj(s)
  time.sleep(0.1)
  listFile = receive_obj(s)
  time.sleep(0.1)

  lfolder.delete(*lfolder.get_children())
  for i in range(len(listFolder)):
    lfolder.insert(parent='', index=i, iid=i, text='', values=listFolder[i])

  lfile.delete(*lfile.get_children())
  for i in range(len(listFile)):
    lfile.insert(parent='', index=i, iid=i, text='', values=listFile[i])

  pass

def toBack(s):
  global path
  if len(pathList): pathList.pop()
  path.delete(0, END)
  stringPath = ''
  if len(pathList): stringPath = pathList[0] + ":\\"
  for i in range(1, len(pathList)): stringPath = stringPath + pathList[i] + '\\'
  path.insert(END, stringPath)
  request = ['file explorer', stringPath]
  requestPath(s, request)
  
  pass

def toRefresh(s):
  requestPath(s, ['file explorer', path.get()])
  pass

def toDeleteFolder(s):
  global path, itemFolder
  stringPath = path.get() + itemFolder + '\\'
  request = ['tree folder', 'delete folder', stringPath]
  send_obj(s, request)
  time.sleep(0.1)
  pass 

def toCopyFile(s):
  global path, itemFile
  stringPath = path.get() + itemFile
  request = ['tree folder', 'copy file', stringPath]
  send_obj(s, request)
  time.sleep(0.1)
  response = receive_obj(s)
  time.sleep(0.5)
  filename = filedialog.asksaveasfilename(initialdir='/', title='Save File', 
      filetypes=(('Text Files', 'txt.*'), ('All Files', '*.*')))
  
  myfile = open(filename, "wb")
  myfile.write(response)
  myfile.close()
  pass

def toDeleteFile(s):
  global path, itemFile
  stringPath = path.get() + itemFile
  request = ['tree folder', 'delete file', stringPath]
  send_obj(s, request)
  time.sleep(0.1)
  pass 

def openFolder(event, s):
  global path, itemFolder
  stringPath = path.get() + itemFolder + '\\'
  pathList.append(itemFolder)
  request = ['file explorer', stringPath]
  path.delete(0, END)
  path.insert(END, stringPath)
  requestPath(s, request)
  pass

def file_explorer(s):
  global path, itemFile, itemFolder, lfolder, lfile

  if check_connect(s) == False: return
  request = ['tree folder']
  send_obj(s, request)
  time.sleep(0.1)
  listDir = receive_obj(s)
  time.sleep(0.1)
  listFolder = receive_obj(s)

  root = Toplevel()
  root.grab_set()
  root.title('File Explorer')
  root.geometry('500x500+200+100')

  ### folder
  my_scrollbar1 = Scrollbar(root, orient=VERTICAL)
  lfolder = Treeview(root, yscrollcommand=my_scrollbar1.set)
  lfolder['columns'] = ('Folder Name', 'Create At')
  lfolder.column('#0', width=0, stretch=NO)    
  lfolder.column('Folder Name', width=200, anchor=CENTER)
  lfolder.column('Create At', width=20, anchor=CENTER)

  lfolder.heading('#0', text='', anchor=CENTER)
  lfolder.heading('Folder Name', text='Folder Name', anchor=CENTER)
  lfolder.heading('Create At', text='Create At', anchor=CENTER)
  lfolder.place(relx=0.04, rely=0.1, relwidth=0.87, relheight=0.38)

  lfolder.bind('<ButtonRelease-1>', selectItemFolder)
  lfolder.bind('<Double-1>', lambda _ : openFolder(_, s))
  for x in range(30):
      lfolder.insert(parent='', index=x, iid=x, text='', values=('notepad', x))

  my_scrollbar1.config(command=lfolder.yview)
  my_scrollbar1.place(relx=0.91, rely=0.1, relwidth=0.05, relheight=0.38)

  ### File
  my_scrollbar2 = Scrollbar(root, orient=VERTICAL)
  lfile = Treeview(root, yscrollcommand=my_scrollbar2.set)
  lfile['columns'] = ('File Name', 'Create At')
  lfile.column('#0', width=0, stretch=NO)    
  lfile.column('File Name', width=200, anchor=CENTER)
  lfile.column('Create At', width=20, anchor=CENTER)

  lfile.heading('#0', text='', anchor=CENTER)
  lfile.heading('File Name', text='File Name', anchor=CENTER)
  lfile.heading('Create At', text='Create At', anchor=CENTER)
  lfile.place(relx=0.04, rely=0.5, relwidth=0.87, relheight=0.38)

  lfile.bind('<ButtonRelease-1>', selectItemFile)
  for x in range(30):
      lfile.insert(parent='', index=x, iid=x, text='', values=('notepad', x))

  my_scrollbar2.config(command=lfile.yview)
  my_scrollbar2.place(relx=0.91, rely=0.5, relwidth=0.05, relheight=0.38)


  Button(root, text='Back', command=lambda: toBack(s)).place(relx=0.04, rely=0.02, relwidth=0.1, relheight=0.05)
  Button(root, text='Refresh', command=lambda: toRefresh(s)).place(relx=0.16, rely=0.02, relwidth=0.1, relheight=0.05)
  path = Entry(root, font='Times 10')
  path.insert(END, "C:\\")
  path.place(relx=0.28, rely=0.02, relwidth=0.67, relheight=0.05)
  
  Button(root, text='Delete Folder', command=lambda: toDeleteFolder(s)).place(relx=0.15, rely=0.9, relwidth=0.2, relheight=0.05)
  Button(root, text='Copy File', command=lambda: toCopyFile(s)).place(relx=0.4, rely=0.9, relwidth=0.2, relheight=0.05)
  Button(root, text='Delete File', command=lambda: toDeleteFile(s)).place(relx=0.65, rely=0.9, relwidth=0.2, relheight=0.05)
  
  root.mainloop()
  pass