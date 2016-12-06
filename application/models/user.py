class User(object):
	"""User"""

	def __init__(self, arg):
		self.id = arg[0]
		self.username = arg[1]
		self.email = arg[2]
		self.password = arg[3]
		self.avatar = arg[4]
		self.create_at = arg[5]