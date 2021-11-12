import pyautogui
import io
import PIL
import sys
import Utils.object_handler as oh
import time
import threading

def send_image(client, img_byte_arr):
	img_size = str(sys.getsizeof(img_byte_arr))
	while len(img_size) < 8:
		img_size = '0' + img_size
	client.sendall(bytes(img_size, 'utf8'))	
	time.sleep(0.001)
	client.sendall(img_byte_arr)

class Streaming(threading.Thread):
	def __init__(self, client) -> None:
		threading.Thread.__init__(self)
		self.is_streaming = False
		self.client = client

	def run(self):
		self.is_streaming = True
		while self.is_streaming:
			temp = pyautogui.screenshot()
			temp.save('temp_image.png')
			img = PIL.Image.open("temp_image.png", mode='r')
			img_byte_arr = io.BytesIO()
			img.save(img_byte_arr, format="PNG")
			img_byte_arr = img_byte_arr.getvalue()
			try:
				send_image(self.client, img_byte_arr)
			except:
				return
	
	def stop_stream(self):
		self.is_screaming = False