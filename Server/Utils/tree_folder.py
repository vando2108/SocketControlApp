import os 
import glob

def list_files(startpath):
	dirs = []
	files = []
	for f in os.listdir(startpath):
		if (os.path.isfile(os.path.join(startpath, f))):
			files.append(f)
		else:
			dirs.append(f)
	return dirs, files

if __name__ == '__main__':
	dirs, files = list_files("e:/")
	print(dirs)
	print(files)