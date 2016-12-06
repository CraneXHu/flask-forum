from flask_script import Manager, Server
from app import app, mysql

manager = Manager(app)
manager.add_command("runserver", Server(host="127.0.0.1", port=5000, use_debugger=True))

@manager.command
def create_table():
	cursor = mysql.get_db().cursor()
	for line in open('application/db/forum.sql'):
		if line.strip():
			cursor.execute(line)
	cursor.close()
	
if __name__ == '__main__':
    manager.run()