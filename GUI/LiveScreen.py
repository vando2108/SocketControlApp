from io import BytesIO
from tkinter import *
from tkinter.ttk import *
import socket
from PIL import ImageTk, Image
from tkinter import filedialog
from SendObject import send_obj, receive_obj, receive_image
from CheckConnect import check_connect
import cv2
import numpy as np
import threading

soc = None

def show_video():
    request = ['screen stream', 'start']
    send_obj(soc, request)
    while True:
        data = receive_image(soc)
        f = open("temp_pic.png", "wb")
        f.write(data)
        f.close()
        img = cv2.imread("temp_pic.png")
        nparr = np.fromstring(data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        scale = 60
        witdh = int(img.shape[1] * scale / 100)
        height = int(img.shape[0] * scale / 100)
        dim = (witdh, height)
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        cv2.imshow('frame', img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            request = ['screen stream', 'stop']
            send_obj(soc, request)
            data = receive_image(soc)
            break

    cv2.destroyAllWindows()

#----------------------------------------------------------------------
def live_screen(s, frame):
    global soc
    soc = s
    show_video()
    #t1 = threading.Thread(target=show_video)
    #t1.start()
    #t1.join()
    #root = Toplevel()
    #root.grab_set()
    #root.title('Pic')
    #root.geometry('700x500+100+100')
    #MainWindow(root)
    #root.mainloop()