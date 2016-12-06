class ResetInfo(object):
	"""User"""

	def __init__(self, arg):
		self.user_id = arg[0]
		self.expiration_time = arg[1]
		self.md5 = arg[2]