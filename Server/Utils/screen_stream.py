import pyautogui
import io
import time
import json

def screen_stream():
	temp = pyautogui.screenshot()
	temp.save('temp_image.jpg')
	img = io.open("temp_image.jpg", mode='r')
	img_byte_arr = io.BytesIO()
	img.save(img_byte_arr, format="JPG")
	img_byte_arr = img_byte_arr.getvalue()
	print(img_byte_arr)
	#while True:
	#	temp = pyautogui.screenshot()
	#	temp.save(r'temp_image.jpg')
	#	img = cv2.imread('temp_image.jpg')
	#	cv2.imshow('frame', img)
	#	if cv2.waitKey(1) & 0xFF == ord('q'):
	#		break
	#cv2.destroyAllWindows()

if __name__ == '__main__':
	screen_stream()