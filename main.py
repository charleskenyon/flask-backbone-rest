from flask import Flask, render_template, abort, request
import json
import sqlite3
import dataset
app = Flask(__name__)

def get_db_table():
	db = dataset.connect('sqlite:///posts.sqlite')
	table = db['posts_table']
	
	return table

def create_and_update_posts():
	counter = 0
	posts = []

	for post in table:
		each_post = {
			'id': counter,
			'Name': post['Name'],
			'Email': post['Email'],
			'Text': post['Text'],
			'Date': post['Date']
		}
		counter += 1
		
		posts.append(each_post)
		
	"""
	for post in posts:
		table.update(post, ['Name', 'Email', 'Text', 'Date'])
	"""
	
	return posts
	
table = get_db_table()
posts = create_and_update_posts()

@app.route('/')
def main_page():
	return render_template('index.html')

@app.route('/posts', methods=['GET'])
def create_json_posts():
	return json.dumps(posts)

@app.route('/posts/<int:post_id>', methods=['GET'])
def create_json_post(post_id):
	get_post = table.find_one(id=post_id)
	
	if get_post is None:
		abort(404)
	
	return json.dumps(posts[post_id])
		
@app.route('/posts', methods=['POST'])
def add_new_json_post():
	if not request.json:
		abort(404)
	
	new_post = {
		'id': posts[-1]['id'] + 1,
		'Name': request.json['Name'],
		'Email': request.json['Email'],
		'Text': request.json['Text'],
		'Date': request.json['Date']
	}
	
	posts.append(new_post)
	table.insert(new_post)
	
	return json.dumps(posts[-1]), 201
	
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
	remove_post = table.find_one(id=post_id)
	
	if remove_post is None:
		abort(404)
		
	remove_post = {
		'id': remove_post['id'],
		'Name': remove_post['Name'],
		'Email': remove_post['Email'],
		'Text': remove_post['Text'],
		'Date': remove_post['Date']
	}
	
	posts.remove(remove_post)
	table.delete(id=post_id)
	
	return json.dumps(posts[post_id])

if __name__ == '__main__':
	app.run(debug=True)