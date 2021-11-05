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
  curItem = lfolder.focus()
  itemFolder = lfolder.item(curItem)['values'][0]
  pass

def selectItemFile(a):
  global itemFile, lfile
  curItem = lfile.focus()
  itemFile = lfile.item(curItem)['values'][0]
  pass

def requestPath(s, request):
  send_obj(s, request)
  listFolder, listFile = receive_obj(s)

  lfolder.delete(*lfolder.get_children())
  for i in range(len(listFolder)):
    lfolder.insert(parent='', index=i, iid=i, text='', values=listFolder[i])

  lfile.delete(*lfile.get_children())
  for i in range(len(listFile)):
    lfile.insert(parent='', index=i, iid=i, text='', values=listFile[i])

  pass

def toBack(s):
  global path
  if len(pathList) > 1: pathList.pop()
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
  request = ['file explorer', 'delete', stringPath]
  send_obj(s, request)
  pass 

def toCopyFile(s):
  global path, itemFile
  stringPath = path.get() + itemFile
  request = ['file explorer', 'copy', stringPath]
  send_obj(s, request)
  response = receive_obj(s)
  filename = filedialog.asksaveasfilename(initialdir='/', title='Save File', 
      filetypes=(('Text Files', 'txt.*'), ('All Files', '*.*')))
  
  myfile = open(filename, "wb")
  myfile.write(response)
  myfile.close()
  pass

def toDeleteFile(s):
  global path, itemFile
  stringPath = path.get() + itemFile
  request = ['file explorer', 'delete', stringPath]
  send_obj(s, request)
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
  request = ['file explorer', "C:\\"]
  requestPath(s, request)

  root = Toplevel()
  root.grab_set()
  root.title('File Explorer')
  root.geometry('700x500+200+100')

  ### folder
  label1 = LabelFrame(root, text='Folder')
  label1.place(relx=0.04, rely=0.1, relwidth=0.9, relheight=0.38)
  my_scrollbar1 = Scrollbar(label1, orient=VERTICAL)
  lfolder = Treeview(label1, yscrollcommand=my_scrollbar1.set)
  lfolder['columns'] = ('Folder Name', 'Create At')
  lfolder.column('#0', width=0, stretch=NO)    
  lfolder.column('Folder Name', width=200, anchor=CENTER)
  lfolder.column('Create At', width=100, anchor=CENTER)

  lfolder.heading('#0', text='', anchor=CENTER)
  lfolder.heading('Folder Name', text='Folder Name', anchor=CENTER)
  lfolder.heading('Create At', text='Create At', anchor=CENTER)
  lfolder.place(relx=0.02, rely=0.02, relwidth=0.92, relheight=0.96)

  lfolder.bind('<ButtonRelease-1>', selectItemFolder)
  lfolder.bind('<Double-1>', lambda _ : openFolder(_, s))
  # for x in range(len(dirs)):
  #   lfolder.insert(parent='', index=x, iid=x, text='', values=dirs[x])

  my_scrollbar1.config(command=lfolder.yview)
  my_scrollbar1.place(relx=0.94, rely=0.02, relwidth=0.04, relheight=0.96)

  ### File
  label2 = LabelFrame(root, text='File')
  label2.place(relx=0.04, rely=0.5, relwidth=0.9, relheight=0.38)
  my_scrollbar2 = Scrollbar(label2, orient=VERTICAL)
  lfile = Treeview(label2, yscrollcommand=my_scrollbar2.set)
  lfile['columns'] = ('File Name', 'Create At')
  lfile.column('#0', width=0, stretch=NO)    
  lfile.column('File Name', width=200, anchor=CENTER)
  lfile.column('Create At', width=100, anchor=CENTER)

  lfile.heading('#0', text='', anchor=CENTER)
  lfile.heading('File Name', text='File Name', anchor=CENTER)
  lfile.heading('Create At', text='Create At', anchor=CENTER)
  lfile.place(relx=0.02, rely=0.02, relwidth=0.92, relheight=0.96)

  lfile.bind('<ButtonRelease-1>', selectItemFile)
  # for x in range(len(files)):
  #     lfile.insert(parent='', index=x, iid=x, text='', values=files[x])

  my_scrollbar2.config(command=lfile.yview)
  my_scrollbar2.place(relx=0.94, rely=0.02, relwidth=0.04, relheight=0.96)


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