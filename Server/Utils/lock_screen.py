import os

def lock_screen():
	cmd = "Rundll32.exe user32.dll,LockWorkStation"
	os.system(cmd)