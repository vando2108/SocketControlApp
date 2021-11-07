import time
import tkinter
from tkinter import *
from tkinter.ttk import *

from PIL import ImageTk, Image
from CheckConnect import check_connect
from SendObject import send_obj, receive_obj, receive_image

check = None

class MainWindow():
  def __init__(self, s, main):
    # canvas for image
    self.canvas = Canvas(main)
    self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
    self.canvas.bind("<Configure>", self.resize)
    self.pic = "screenshot.png"
    # get images
    request = ['screen stream']
    send_obj(s, request)
    response = receive_image(s)
    f = open(self.pic, "wb")
    f.write(response)
    f.close()
    # images
    self.photo = Image.open(self.pic).resize((490, 400), Image.ANTIALIAS)
    self.img = ImageTk.PhotoImage(self.photo)

    # set first image on canvas
    self.canvas_img = self.canvas.create_image(0, 0, anchor = NW, image = self.img)
    pass

  # ----
  def resize(self, event):
    img = Image.open(self.pic).resize(
        (event.width, event.height), Image.ANTIALIAS
    )
    self.img = ImageTk.PhotoImage(img)
    self.canvas.itemconfig(self.canvas_img, image=self.img)
    pass

# ------------


def turnOn(s, frame):
  global check
  check = True
  while check:
    # check = False
    MainWindow(s, frame)
  pass

def turnOff(s):
  global check
  check = False

def live_screen(s, frame):
  if check_connect(s) == False: return
  root = frame
  for widget in root.winfo_children():
    widget.destroy()
  root.configure(text='Screen')

  make_frame = LabelFrame(root, text='Screen', width=500, height=400)
  make_frame.place(relx=0.05, rely = 0.05, relwidth=0.9, relheight=0.8)

  Button(root, text='Turn On', command=lambda: turnOn(
      s, make_frame)).place(relx=0.2, rely=0.9, relwidth=0.2, relheight=0.05)
  Button(root, text='Turn Off', command=lambda: turnOff(
      s)).place(relx=0.6, rely=0.9, relwidth=0.2, relheight=0.05)
  
  # root.mainloop()
  pass