#coding:utf-8
import datetime

def post_time(date):
	now = datetime.datetime.now()
	if date.year < now.year:
		return "%d年前" % (now.year - date.year)
	elif date.month < now.month:
		return "%d月前" % (now.month - date.month)
	elif date.day < now.day:
		return "%d天前" % (now.day - date.day)
	elif date.hour < now.hour:
		return "%d小时前" % (now.hour - date.hour)
	elif date.minute < now.minute:
		return "%d分前" % (now.minute - date.minute)
	else:
		return "%d秒前" % (now.second - date.second)
