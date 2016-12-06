class Comment(object):
	"""docstring for Comments"""

	def __init__(self, arg):
		self.id = arg[0]
		self.articleId = arg[1]
		self.username = arg[2]
		self.content = arg[3]
		self.create_at = arg[4]
		