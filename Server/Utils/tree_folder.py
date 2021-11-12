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
			files.append([str(f), date, os.path.getsize(file_path)])
		else:
			dirs.append([str(f), date, os.path.getsize(file_path)])

	return dirs, files