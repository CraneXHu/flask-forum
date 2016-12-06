from application.models.user import User
from application.models.article import Article
from application.models.comment import Comment
from application.models.reset_info import ResetInfo
from md5_util import get_md5_value

class DBHelper(object):
	"""docstring for DBHelper"""
	mysql = None

	@staticmethod
	def init(sql):
		DBHelper.mysql = sql

	@staticmethod
	def get_user_count():
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'select count(*) from user'
		cursor.execute(sql)
		result = cursor.fetchone()
		return result[0]

	@staticmethod
	def get_user(email):
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'select * from user where email=%s'
		cursor.execute(sql, email)
		user = cursor.fetchone()
		if user:
			return User(user)
		return None

   	@staticmethod
	def get_user_by_name(username):
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'select * from user where username=%s'
		cursor.execute(sql, username)
		user = cursor.fetchone()
		if user:
			return User(user)
		return None

	@staticmethod
	def create_user(username, email, password):
		password = get_md5_value(password)
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'insert into user (username, email, password) values (%s, %s, %s)'
		cursor.execute(sql, (username, email, password))
		DBHelper.mysql.get_db().commit()

	@staticmethod
	def update_user(id, username):
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'update user set username=%s where id=%s'
		cursor.execute(sql, (username, id))
		DBHelper.mysql.get_db().commit()

	@staticmethod
	def update_password(id, password):
		password = get_md5_value(password)
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'update user set password=%s where id=%s'
		cursor.execute(sql, (password, id))
		DBHelper.mysql.get_db().commit()

	@staticmethod
	def update_avatar(id, avatar):
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'update user set avatar=%s where id=%s'
		cursor.execute(sql, (avatar, id))
		DBHelper.mysql.get_db().commit()

	@staticmethod
	def update_social_account(user_id, github, weibo, twitter):
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'insert into social_account (user_id, github, weibo, twitter) values(%s, %s, %s, %s) on duplicate key update github=values(github), weibo=values(weibo), twitter=values(twitter)'
		cursor.execute(sql, (user_id, github, weibo, twitter))
		DBHelper.mysql.get_db().commit()

	@staticmethod
	def get_articles(index):
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'select * from article order by article.create_at desc limit %s, %s'
		cursor.execute(sql, (index, 20))
		articleTuples = cursor.fetchall()
		articles = []
		for article in articleTuples:
			articles.append(Article(article))
		if len(articles) == 0:
			articles = None
		return articles

	@staticmethod
	def get_articles_by_username(username, index):
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'select * from article where username=%s order by article.create_at desc limit %s, %s'
		cursor.execute(sql, (username, index, 20))
		articleTuples = cursor.fetchall()
		articles = []
		for article in articleTuples:
			articles.append(Article(article))
		if len(articles) == 0:
			articles = None
		return articles

	@staticmethod
	def get_article_count():
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'select count(*) from article'
		cursor.execute(sql)
		result = cursor.fetchone()
		return result[0]

	@staticmethod
	def get_articles_by_tag(tag, index):
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'select * from article where tag=%s order by article.create_at desc limit %s, %s'
		cursor.execute(sql, (tag, index, 20))
		articleTuples = cursor.fetchall()
		articles = []
		for article in articleTuples:
			articles.append(Article(article))
		if len(articles) == 0:
			articles = None
		return articles

	@staticmethod
	def get_articles_by_comments(username, index):
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'select * from article where id in (select articleId from comment where username=%s) limit %s, %s'
		cursor.execute(sql, (username, index, 20))
		articleTuples = cursor.fetchall()
		articles = []
		for article in articleTuples:
			articles.append(Article(article))
		if len(articles) == 0:
			articles = None
		return articles

	@staticmethod
	def get_article(id):
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'select * from article where id=%s'
		cursor.execute(sql, id)
		article = cursor.fetchone()
		article = Article(article)
		return article

	@staticmethod
	def create_article(username, tag, title, content):
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'insert into article (username, tag, title, content) values (%s, %s, %s, %s)'
		cursor.execute(sql, (username, tag, title, content))
		DBHelper.mysql.get_db().commit()

	@staticmethod
	def update_comment_count(id):
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'update article set comment_count = comment_count+1 where id = %s'
		cursor.execute(sql, id)
		DBHelper.mysql.get_db().commit()

	@staticmethod
	def get_comment_count():
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'select count(*) from comment'
		cursor.execute(sql)
		result = cursor.fetchone()
		return result[0]

	@staticmethod
	def get_comments(id):
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'select * from comment where ArticleId=%s'
		cursor.execute(sql, id)
		commentTuples = cursor.fetchall()
		comments = []
		for comment in commentTuples:
			comments.append(Comment(comment))
		if len(comments) == 0:
			comments = None
		return comments

	@staticmethod
	def get_comments_by_username(username, index):
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'select * from comment where username=%s limit %s, %s'
		cursor.execute(sql, (username, index, 20))
		commentTuples = cursor.fetchall()
		comments = []
		for comment in commentTuples:
			comments.append(Comment(comment))
		if len(comments) == 0:
			comments = None
		return comments

	@staticmethod
	def get_article_comment_count(id):
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'select count(*) from comment where ArticleId=%s'
		cursor.execute(sql, id)
		result = cursor.fetchone()
		return result[0]

	@staticmethod
	def create_comment(articleId, username, comment):
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'insert into comment (articleId, username, content) values (%s, %s, %s)'
		cursor.execute(sql, (articleId, username, comment))
		DBHelper.mysql.get_db().commit()

	@staticmethod
	def get_notifications(username):
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'select article.id, article.title, comment.username, comment.content, comment.create_at from article, comment where article.id=comment.articleId and article.username=%s order by comment.create_at desc'
		cursor.execute(sql, username)
		results = cursor.fetchall()
		comments = []
		for result in results:
			comment = {}
			comment['articleId'] = result[0]
			comment['title'] = result[1]
			comment['username'] = result[2]
			comment['content'] = result[3]
			comment['create_at'] = result[4]
			comments.append(comment)
		if len(comments) == 0:
			comments = None
		return comments

	@staticmethod
	def create_reset_info(user_id, expiration_time, md5):
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'insert into reset_info (user_id, expiration_time, md5) values (%s, %s, %s)'
		cursor.execute(sql, (user_id, expiration_time, md5))
		DBHelper.mysql.get_db().commit()

	@staticmethod
	def get_reset_info(md5):
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'select * from reset_info where md5=%s'
		cursor.execute(sql, md5)
		result = cursor.fetchone()
		return ResetInfo(result)

	@staticmethod
	def delete_reset_info(md5):
		cursor = DBHelper.mysql.get_db().cursor()
		sql = 'delete from reset_info where md5=%s'
		cursor.execute(sql, md5)
		DBHelper.mysql.get_db().commit()