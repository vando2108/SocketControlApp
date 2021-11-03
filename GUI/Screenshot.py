from tkinter import *
from tkinter.ttk import *
import socket
from PIL import ImageTk, Image
from tkinter import filedialog
from SendObject import send_obj, receive_obj
from CheckConnect import check_connect
import time

soc = None

class MainWindow():

    def __init__(self, main):

        # canvas for image
        self.canvas = Canvas(main)
        self.canvas.place(relx=0.05, rely=0.1, relwidth=0.7, relheight=0.8)
        self.canvas.bind("<Configure>", self.resize)
        self.pic = "screenshot.png"
        # get images
        request = ['screenshot']
        send_obj(soc, request)
        time.sleep(0.01)
        data = receive_obj(soc)
        f = open(self.pic, "wb")
        f.write(data)
        f.close()
        # images
        self.photo = Image.open(self.pic).resize((490, 400), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.photo)

        # set first image on canvas
        self.canvas_img = self.canvas.create_image(0, 0, anchor = NW, image = self.img)

        # button to change image
        Button(main, text='TakeScreenshot', command=self.takeScreenshot).place(relx=0.8, rely=0.1, relwidth=0.15, relheight=0.5)
        Button(main, text='Save', command=self.saveScreenshot).place(relx=0.8, rely=0.65, relwidth=0.15, relheight=0.25)

    #----------------
    def resize(self, event):
        img = Image.open(self.pic).resize(
            (event.width, event.height), Image.ANTIALIAS
        )
        self.img = ImageTk.PhotoImage(img)
        self.canvas.itemconfig(self.canvas_img, image=self.img)
        pass

    def takeScreenshot(self):
        if check_connect(soc) == False: return
        request = ['screenshot']
        send_obj(soc, request)
        time.sleep(0.01)
        data = receive_obj(soc)
        f = open(self.pic, "wb")
        f.write(data)
        f.close()

        self.photo = Image.open(self.pic).resize((490, 400), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.photo)
        self.canvas.itemconfig(self.canvas_img, image=self.img)
        pass

    def saveScreenshot(self):
        file_path = filedialog.asksaveasfilename(defaultextension = '.png')
        self.photo.save(file_path)
        pass

#----------------------------------------------------------------------
def screenshot(s):
    soc = s
    if check_connect(soc) == False: return
    root = Toplevel()
    root.grab_set()
    root.title('Pic')
    root.geometry('700x500+100+100')
    MainWindow(root)
    root.mainloop()
