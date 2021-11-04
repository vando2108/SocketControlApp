from tkinter import *
from tkinter import ttk

def selectItem(a):
    curItem = tree.focus()
    print(tree.item(curItem)['values'][1])

def openFolder(event):
  curItem = tree.focus()
  print(tree.item(curItem)['values'][1])


root = Tk()
tree = ttk.Treeview(root, columns=("size", "modified"))
tree["columns"] = ("date", "time", "loc")

tree.column("date", width=65)
tree.column("time", width=40)
tree.column("loc", width=100)

tree.heading("date", text="Date")
tree.heading("time", text="Time")
tree.heading("loc", text="Loc")
tree.bind('<ButtonRelease-1>', selectItem)
tree.bind('<Double-1>', lambda _ : openFolder(_))

tree.insert("","end",text = "Name",values = ("Date","Time","Loc"))

tree.grid()
root.mainloop()