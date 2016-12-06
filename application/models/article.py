class Article(object):
	"""docstring for Article"""

	def __init__(self, arg):
		self.id = arg[0]
		self.username = arg[1]
		self.tag = arg[2]
		self.title = arg[3]
		self.content = arg[4]
		self.comment_count = arg[5]
		self.create_at = arg[6]