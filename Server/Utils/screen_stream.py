import pyautogui
import io
import time
import json
import PIL
import sys
import Utils.object_handler as oh
import time

def send_image(client, img_byte_arr):
	img_size = str(sys.getsizeof(img_byte_arr))
	while len(img_size) < 8:
		img_size = '0' + img_size
	client.sendall(bytes(img_size, 'utf8'))	
	time.sleep(0.001)
	client.sendall(img_byte_arr)

def screen_stream(client):
	temp = pyautogui.screenshot()
	temp.save('temp_image.png')
	img = PIL.Image.open("temp_image.png", mode='r')
	img_byte_arr = io.BytesIO()
	img.save(img_byte_arr, format="PNG")
	img_byte_arr = img_byte_arr.getvalue()
	send_image(client, img_byte_arr)

	#while True:
	#	temp = pyautogui.screenshot()
	#	temp.save('temp_image.png')
	#	img = PIL.Image.open("temp_image.png", mode='r')
	#	img_byte_arr = io.BytesIO()
	#	img.save(img_byte_arr, format="PNG")
	#	img.seek(0)
	#	img_byte_arr = img_byte_arr.getvalue()
	#	client.sendall(bytes(str(sys.getsizeof(img_byte_arr)), "utf8"))
	#	client.sendall(img_byte_arr)