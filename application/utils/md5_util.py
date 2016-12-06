import hashlib

def get_md5_value(src):
	my_md5 = hashlib.md5()
	my_md5.update(src)
	return my_md5.hexdigest()