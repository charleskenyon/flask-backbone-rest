from flask import Flask, render_template
import json
import sqlite3
app = Flask(__name__)

@app.route('/')
def main_page():
	return render_template('index.html')

@app.route('/posts')
def create_json():
	connection = sqlite3.connect("posts.sqlite")
	curs = connection.cursor()
	
	curs.execute('SELECT * FROM posts_table')
	posts = [dict(Name=row[0], Text=row[1], Date=row[2], Email=row[3]) for row in curs.fetchall()]
	connection.close()
	
	return json.dumps(posts)

if __name__ == '__main__':
	app.run(debug=True)