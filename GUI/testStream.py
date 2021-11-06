import socket
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

soc = None

class Page(Frame):
  def __init__(self, parent, soc):
    self.root = parent
    self.s = soc
    # request = ['file explorer', "C:\\"]
    # send_obj(soc, request)
    # self.dirs, self.files = receive_obj(soc)
    self.nodes = {}
    # self.dirs = [['a', 'b', 'c'], ['d', 'e', 'f']]
    # self.files = [['r', 'b', 'a'], ['q', 'e', 'd']]

    Button(self.root, text='Back', command=self.toBack).place(relx=0.04, rely=0.02, relwidth=0.1, relheight=0.05)
    Button(self.root, text='Refresh', command=self.toRefresh).place(relx=0.16, rely=0.02, relwidth=0.1, relheight=0.05)
    self.path = Entry(self.root, font='Times 10')
    self.path.insert(END, "D:\\")
    self.path.place(relx=0.28, rely=0.02, relwidth=0.62, relheight=0.05)
  
    self.frame = LabelFrame(self.root, text='File Explorer')
    self.frame.place(relx=0.04, rely=0.1, relwidth=0.9, relheight=0.85)

    ###  Menu
    self.popup = Menu(self.root, tearoff=0)
    self.popup.add_command(label="Delete", command=self.delete)
    self.popup.add_command(label="Copy", command=self.copy)
    self.popup.add_command(label="Download", command=self.download)
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
    # self.tree['columns'] = ('Directory', 'Last modified time', 'Size')
    self.tree['columns'] = ('Last modified time', 'Size')
    self.tree.column('#0', width=300, stretch=NO)    
    # self.tree.column('Directory', width=300, anchor=CENTER)
    self.tree.column('Last modified time', width=50, anchor='w')
    self.tree.column('Size', width=50, anchor=CENTER)

    self.tree.heading('#0', text='Directory', anchor='w')
    # self.tree.heading('Directory', text='Directory', anchor=CENTER)
    self.tree.heading('Last modified time', text='Last modified time', anchor=CENTER)
    self.tree.heading('Size', text='Size', anchor=CENTER)
    self.tree.place(relx=0.02, rely=0.02, relwidth=0.92, relheight=0.96)

    # self.tree.bind('<ButtonRelease-1>', self.selectItem)
    # self.tree.bind('<Double-1>', self.openFolder)
    # self.tree.bind('<Button-3>', do_popup)
    # for x in range(len(self.dirs)):
    #   self.tree.insert(parent='', index=x, iid=x, text='', values=self.dirs[x])
    abspath = 'D:\\'
    self.insert_node('', [abspath, 'thurs', '30kb'], abspath)
    self.tree.bind('<<TreeviewOpen>>', self.open_node)

    scroll.config(command=self.tree.yview)
    scroll.place(relx=0.94, rely=0.02, relwidth=0.04, relheight=0.96)
    
    pass

  def insert_node(self, parent, value, abspath):
    # print(abspath)
    node = self.tree.insert(parent, 'end', text=value[0], values=(value[1], value[2]), open=False)
    if abspath:
      self.nodes[node] = abspath
      self.tree.insert(node, 'end')
    pass

  def open_node(self, event):
    
    pass

  def getPath(self, id):
    
    pass

  def requestPath(request):
    pass

  def toBack(self):
   
    pass

  def toRefresh():
    print('refresh')
    pass
  
  def openFolder():

    pass

  def selectItem():
    pass

  def delete(self):
    
    pass

  def copy(self):
    
    pass

  def download(self):
    print(self.popup.selection)
    pass

# ---------------------

def file_explorer(s):
  # if check_connect(s) == False: return
  root = Tk()
  root.title('File Explorer')
  root.geometry('800x500+200+100')
  Page(root, s)
  root.mainloop()


if __name__ == "__main__":
  file_explorer(None)
  pass