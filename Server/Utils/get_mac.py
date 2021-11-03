import re, uuid

def get_mac():
	return ':'.join(re.findall('..', '%012x' % uuid.getnode()))