#coding:utf-8
import os
from flask import Flask
from flask import redirect, url_for, request, render_template
from flask import send_from_directory
from werkzeug.utils import secure_filename
from flaskext.mysql import MySQL

from application.models.user import User
from application.models.article import Article
from application.models.comment import Comment

from application.utils.account import Account
from application.utils.db_helper import DBHelper
from application.utils.date import post_time
from application.utils.filters import first_upper, first_lower

from application.config import Config

import sys

reload(sys)

sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config.from_object(Config)
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'mysql_password'
# app.config['MYSQL_DATABASE_DB'] = 'forum'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['SECRET_KEY'] = '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83'

env = app.jinja_env
env.filters['first_upper'] = first_upper
env.filters['first_lower'] = first_lower

mysql = MySQL()
mysql.init_app(app)
DBHelper.init(mysql)


PAGE_SIZE = 20

@app.route('/')
def index():
    user = None
    if Account.isLogin():
        user = Account.get_current_user()
    articles = DBHelper.get_articles(0)
    if articles:
        for article in articles:
            article.time = post_time(article.create_at)
    statistics = {}
    statistics['user_count'] = DBHelper.get_user_count()
    statistics['article_count'] = DBHelper.get_article_count()
    statistics['comment_count'] = DBHelper.get_comment_count()
    return render_template('index.html', user = user, articles = articles, tag = 'all', statistics = statistics)

@app.route('/article', methods=['GET','POST'])
def article():
    user = None
    if Account.isLogin():
        user = Account.get_current_user()
    statistics = {}
    statistics['user_count'] = DBHelper.get_user_count()
    statistics['article_count'] = DBHelper.get_article_count()
    statistics['comment_count'] = DBHelper.get_comment_count()
    if request.method == 'GET':
        return render_template('article.html', user = user, statistics = statistics)
    else:
        DBHelper.create_article(user.username, request.form['tag'],request.form['title'], request.form['contentArea'])
        return redirect(url_for('index'))

@app.route('/<tag>')
def classify(tag):
    user = None
    message = None
    if Account.isLogin():
        user = Account.get_current_user()
    articles = DBHelper.get_articles_by_tag(tag,0)
    statistics = {}
    statistics['user_count'] = DBHelper.get_user_count()
    statistics['article_count'] = DBHelper.get_article_count()
    statistics['comment_count'] = DBHelper.get_comment_count()
    return render_template('index.html', user = user, articles = articles, tag = tag, statistics = statistics)

@app.route('/discussion/<int:id>', methods=['GET','POST'])
def discussion(id):
    user = None
    message = None
    isLogin = Account.isLogin()
    if isLogin:
        user = Account.get_current_user()
    if request.method == 'POST':
        if isLogin:
            DBHelper.create_comment(id, user.username, request.form['content'])
            DBHelper.update_comment_count(id)
        else:
            message = 'please login'
    article = DBHelper.get_article(id)
    article.time = post_time(article.create_at)
    comments = DBHelper.get_comments(id)
    if comments:
        for comment in comments:
            comment.time = post_time(comment.create_at)
    statistics = {}
    statistics['user_count'] = DBHelper.get_user_count()
    statistics['article_count'] = DBHelper.get_article_count()
    statistics['comment_count'] = DBHelper.get_comment_count()
    return render_template('discussion.html', user = user, article = article, comments = comments, statistics = statistics, message = message)

@app.route('/notification')
def notification():
    user = Account.get_current_user()
    comments = DBHelper.get_notifications(user.username)
    if comments:
        for comment in comments:
            comment['time'] = post_time(comment['create_at'])
            comment_user = DBHelper.get_user_by_name(comment['username'])
            comment['avatar'] = comment_user.avatar
    return render_template('notification.html', user = user, comments = comments)

@app.route('/user/<username>')
def user(username):
    user = Account.get_current_user()
    articles = DBHelper.get_articles_by_username(username, 0)
    if articles:
        for article in articles:
            article.time = post_time(article.create_at)
    comments = DBHelper.get_comments_by_username(username, 0)
    commentted_articles = DBHelper.get_articles_by_comments(username, 0)
    if comments:
        index = 0
        for comment in comments:
            comment.article_title = commentted_articles[index].title
            comment.time = post_time(comment.create_at)
            index = index + 1
    return render_template('user.html', user = user, articles = articles, comments = comments)

@app.route('/setting', methods=['GET','POST'])
def setting():
    user = Account.get_current_user()
    if request.method == 'POST':
        DBHelper.update_user(user.id, request.form['username'])
        DBHelper.update_social_account(user.id, request.form['github'], request.form['weibo'], request.form['twitter'])
        user = Account.get_current_user()
    return render_template('setting.html', user = user)

@app.route('/avatar/<filename>')
def avatar(filename):
    return send_from_directory('avatar', filename)

@app.route('/setting/avatar', methods=['POST'])
def setting_avatar():
    user = Account.get_current_user()
    if request.method == 'POST':
        file = request.files['avatar']
        file_name = secure_filename(file.filename)
        file.save(os.path.join('avatar', file_name))
        DBHelper.update_avatar(user.id, '/avatar/' + file_name)
    user = Account.get_current_user()
    return render_template('setting.html', user = user)

@app.route('/setting/password', methods=['POST'])
def setting_password():
    user = Account.get_current_user()
    if request.method == 'POST':
        password_current = request.form['password_current']
        password_new = request.form['password_new']
        if password_current == user.password:
            DBHelper.update_password(user.id, password_new)
    return render_template('setting.html', user = user)

@app.route('/account/signup', methods=['GET', 'POST'])
def signup():
    if Account.isLogin() :
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('register.html')
    else:
        if Account.isRegister(request.form['email']):
            return render_template('register.html')
        else:
            Account.register(request.form['username'],request.form['email'],request.form['password'])
            return redirect(url_for('login'))

@app.route('/account/login', methods=['GET', 'POST'])
def login():
    message = None
    if Account.isLogin() :
        return redirect(url_for('index'))
    if request.method == 'POST':
        isLogin = Account.login(request.form['email'], request.form['password'])
        if isLogin:
            return redirect(url_for('index'))
        else :
            message = '账号或密码错误'
            return render_template('login.html', message = message)
    else :
        return render_template('login.html', message = None)

@app.route('/account/logout')
def logout():
    Account.logout()
    return redirect(url_for('index'))

@app.route('/account/reset', methods=['GET', 'POST'])
def set_reset_info():
    msg = None
    if request.method == 'POST':
        user = DBHelper.get_user(request.form['email'])
        if user:
            Account.send_email(user)
            msg = "已发送到邮箱"
        else:
            msg = "没有该用户"
    return render_template('reset_info.html', msg = msg)

@app.route('/account/reset/<md5>', methods=['GET', 'POST'])
def reset(md5):
    msg = None
    if request.method == 'POST':
        info = DBHelper.get_reset_info(md5)
        if info:
            DBHelper.delete_reset_info(md5)
            DBHelper.update_password(info.user_id, request.form['password'])
            msg = "设置成功"
        else:
            msg = "链接错误"
    return render_template('reset.html', msg)

if __name__ == '__main__':
	app.run()