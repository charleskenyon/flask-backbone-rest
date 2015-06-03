from flask import Flask, render_template, abort, request, g, Response
import json
import sqlite3
import dataset
app = Flask(__name__)

def create_and_update_posts():
	posts = []

	for post in g.table:
		each_post = {
			'id': post['id'],
			'Name': post['Name'],
			'Email': post['Email'],
			'Text': post['Text'],
			'Date': post['Date']
		}
		
		posts.append(each_post)
	
	return posts

@app.before_request
def before_request():
	g.db = dataset.connect('sqlite:///posts.sqlite')
	g.table = g.db['posts_table']
	g.posts = create_and_update_posts()

@app.route('/')
def main_page():
	return render_template('index.html')

@app.route('/posts', methods=['GET'])
def create_json_posts():
	return Response(json.dumps(g.posts), mimetype='application/json')

@app.route('/posts/<int:post_id>', methods=['GET'])
def create_json_post(post_id):
	get_post = g.table.find_one(id=post_id)
	
	if get_post is None:
		abort(404)
		
	get_post = {
		'id': get_post['id'],
		'Name': get_post['Name'],
		'Email': get_post['Email'],
		'Text': get_post['Text'],
		'Date': get_post['Date']
	}
	
	return Response(json.dumps(get_post), mimetype='application/json')
		
@app.route('/posts', methods=['POST'])
def add_new_json_post():
	if not request.json:
		abort(404)
	
	new_post = {
		'id': g.posts[-1]['id'] + 1,
		'Name': request.json['Name'],
		'Email': request.json['Email'],
		'Text': request.json['Text'],
		'Date': request.json['Date']
	}
	
	g.posts.append(new_post)
	g.table.insert(new_post)
	
	return Response(json.dumps(g.posts[-1]), 201, mimetype='application/json')
	
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
	remove_post = g.table.find_one(id=post_id)
	
	if remove_post is None:
		abort(404)
		
	remove_post = {
		'id': remove_post['id'],
		'Name': remove_post['Name'],
		'Email': remove_post['Email'],
		'Text': remove_post['Text'],
		'Date': remove_post['Date']
	}
	
	g.posts.remove(remove_post)
	g.table.delete(id=post_id)
	
	return Response(json.dumps(g.posts), mimetype='application/json')

if __name__ == '__main__':
	app.run(debug=True)