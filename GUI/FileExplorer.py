import socket
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from CheckConnect import check_connect

from SendObject import send_obj, receive_obj

soc = None

class Page(Frame):
  def __init__(self, parent, soc):
    self.root = parent
    self.s = soc
    self.nodes = {}

    Label(self.root, text='Path: ').place(relx=0.05, rely=0.02, relwidth=0.05, relheight=0.05)
    self.path = Entry(self.root, font='Times 10')
    self.path.insert(END, "D:\\")
    self.path.place(relx=0.12, rely=0.02, relwidth=0.5, relheight=0.05)
  
    self.frame = LabelFrame(self.root, text='File Explorer')
    self.frame.place(relx=0.04, rely=0.1, relwidth=0.9, relheight=0.85)

    ###  Menu
    self.popup = Menu(self.frame, tearoff=0)
    self.popup.add_command(label="Delete", command=self.delete)
    self.popup.add_command(label="Copy", command=self.copy)
    #self.popup.add_separator()

    def do_popup(event):
      try:
        self.popup.selection = self.tree.set(self.tree.identify_row(event.y))
        self.popup.post(event.x_root, event.y_root)
      finally:
        self.popup.grab_release()
    
    ### Tree
    scroll = Scrollbar(self.frame, orient=VERTICAL)
    self.tree = Treeview(self.frame, yscrollcommand=scroll.set)
    self.tree['columns'] = ('Last modified time', 'Size')
    self.tree.column('#0', width=450, stretch=NO, anchor='w') 
    self.tree.column('Last modified time', width=120, anchor='w')
    self.tree.column('Size', width=30, anchor=CENTER)

    self.tree.heading('#0', text='Directory', anchor=CENTER)
    self.tree.heading('Last modified time', text='Last modified time', anchor=CENTER)
    self.tree.heading('Size', text='Size', anchor=CENTER)
    self.tree.place(relx=0.02, rely=0.02, relwidth=0.92, relheight=0.96)

    self.tree.bind('<ButtonRelease-1>', self.selectItem)
    self.tree.bind('<Button-3>', do_popup)
    abspath = 'D:'
    self.insert_node('', (abspath, '', ''), abspath+'\\')
    self.tree.bind('<<TreeviewOpen>>', self.open_node)

    scroll.config(command=self.tree.yview)
    scroll.place(relx=0.94, rely=0.02, relwidth=0.04, relheight=0.96)
    
    pass

  def insert_node(self, parent, value, abspath):
    # print(abspath)
    node = self.tree.insert(parent, 'end', text=value[0], values=[value[1], '30kb'], open=False)
    if abspath:
      self.nodes[node] = abspath
      self.tree.insert(node, 'end')
    pass

  def open_node(self, event):
    node = self.tree.focus()
    # print(self.tree.item(self.tree.selection()[0])['text'])
    abspath = self.nodes.pop(node, None)
    if abspath:
      request = ['file explorer', abspath]
      send_obj(self.s, request)
      dirs, files = receive_obj(self.s)

      # dirs
      self.tree.delete(self.tree.get_children(node))
      for p in dirs:
        self.insert_node(node, p, abspath+'\\'+p[0])

      # files
      for p in files:
        self.insert_node(node, p, None)
    pass

  def selectItem(self, event):
    node = self.tree.focus()
    stringPath = self.getPath(node)
    self.path.delete(0, END)
    self.path.insert(END, stringPath)
    pass

  def getPath(self, id):
    stringPath = self.tree.item(id)['text']
    id = self.tree.parent(id)
    while self.tree.item(id)['text'] != '':
      stringPath = self.tree.item(id)['text'] + '\\' + stringPath
      id = self.tree.parent(id)
    return stringPath
    pass

  def delete(self):
    stringPath = self.path.get()
    request = ['file explorer', 'delete', stringPath]
    send_obj(self.s, request)
    pass

  def copy(self):
    stringPath = self.path.get()
    request = ['file explorer', 'copy', stringPath]
    send_obj(self.s, request)
    response = receive_obj(self.s)
    filename = filedialog.asksaveasfilename(initialdir='/', title='Save File', 
        filetypes=(('Text Files', 'txt.*'), ('All Files', '*.*')))
    
    myfile = open(filename, "wb")
    myfile.write(response)
    myfile.close()
    pass

# ---------------------

def file_explorer(s, frame):
  if check_connect(s) == False: return
  root = frame
  for widget in root.winfo_children():
    widget.destroy()
  root.configure(text='Tree Folder')
  Page(root, s)

# if __name__ == "__main__":
#   file_explorer(None)
#   pass