import os 
import glob
import time

def list_files(startpath):
	dirs = []
	files = []
	for f in os.listdir(startpath):
		file_path = os.path.join(startpath, f)
		date = time.ctime(os.path.getctime(file_path))
		if (os.path.isfile(file_path)):
			files.append([f, date])
		else:
			dirs.append([f, date])
	return dirs, files