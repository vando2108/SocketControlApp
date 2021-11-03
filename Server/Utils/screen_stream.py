import pyautogui
import cv2
import io
import time
import json
import PIL
import sys

def screen_stream(client):
#	temp = pyautogui.screenshot()
#	temp.save('temp_image.png')
#	img = PIL.Image.open("temp_image.png", mode='r')
#	img_byte_arr = io.BytesIO()
#	img.save(img_byte_arr, format="PNG")
#	img_byte_arr = img_byte_arr.getvalue()
#	client.sendall(img_byte_arr)

	while True:
		temp = pyautogui.screenshot()
		temp.save('temp_image.png')
		img = PIL.Image.open("temp_image.png", mode='r')
		img_byte_arr = io.BytesIO()
		img.save(img_byte_arr, format="PNG")
		img.seek(0)
		img_byte_arr = img_byte_arr.getvalue()
		client.sendall(bytes(str(sys.getsizeof(img_byte_arr)), "utf8"))
		client.sendall(img_byte_arr)

if __name__ == '__main__':
	screen_stream()