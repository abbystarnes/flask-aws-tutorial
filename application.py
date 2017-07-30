'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS

Author: Scott Rodkey - rodkeyscott@gmail.com

Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''
import sqlite3
import os
from flask import Flask, render_template, request, jsonify, send_file, json
from werkzeug import secure_filename
from application import db
from application.models import Data
from application.forms import EnterDBInfo, RetrieveDBInfo


# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(APP_ROOT, 'static/index.html')
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'

@application.route('/', methods =['GET'])
def index():
    return send_file(INDEX)
@application.route('/api/posts', methods =['GET', 'POST'])
def collection():
    if request.method == 'GET':
        try:
            with sqlite3.connect('reddit.db') as connection:
                connection.row_factory = dict_factory
                cursor = connection.cursor()
                cursor.execute("""
                SELECT * FROM posts;
                """)
                posts = cursor.fetchall()
        except:
            result = {'status': 0, 'message': 'error'}
        return json.dumps(posts)
    elif request.method == 'POST':
        data = request.get_json(force=True)
        result = add_post(data['title'], data['body'], data['author'], data['image_url'])
        return jsonify(result)
@application.route('/api/posts/<post_id>', methods = ['GET', 'PATCH', 'DELETE'])
def resource(post_id):
    if request.method == 'GET':
        try:
            with sqlite3.connect('reddit.db') as connection:
                connection.row_factory = dict_factory
                cursor = connection.cursor()
                cursor.execute("""
                SELECT * FROM posts WHERE id = ?;
                """, (post_id))
                result = cursor.fetchall()
        except:
            result = {'status': 0, 'message': 'error'}
        return json.dumps(post)
    elif request.method == 'PATCH':
        data = request.get_json(force=True)
        result = edit_post(data['title'], data['body'], data['author'], data['image_url'], data['id'])
        return jsonify(result)
    elif request.method == 'DELETE':
        try:
            with sqlite3.connect('reddit.db') as connection:
                connection.row_factory = dict_factory
                cursor = connection.cursor()
                cursor.execute("""
                DELETE FROM posts WHERE id = ?;
                """, (post_id))
                result = cursor.fetchall()
        except:
            result = {'status': 0, 'message': 'error'}
        return jsonify(result)
@application.route('/api/posts/<post_id>/votes', methods = ['POST', 'DELETE'])
def votes(post_id):
    if request.method == 'POST':

        try:
            with sqlite3.connect('reddit.db') as connection:
                connection.row_factory = dict_factory
                cursor = connection.cursor()
                cursor.execute("""
                UPDATE posts SET vote_count = vote_count + 1 WHERE id = ?;
                """, (post_id))
                result = cursor.fetchall()
        except:
            result = {'status': 0, 'message': 'error'}
        return json.dumps(result)
    elif request.method == 'DELETE':
        try:
            with sqlite3.connect('reddit.db') as connection:
                connection.row_factory = dict_factory
                cursor = connection.cursor()
                cursor.execute("""
                UPDATE posts SET vote_count = vote_count - 1 WHERE id = ?;
                """, (post_id))
                result = cursor.fetchall()
        except:
            result = {'status': 0, 'message': 'error'}
        return json.dumps(result)
@application.route('/api/posts/<post_id>/comments', methods = ['GET', 'POST'])
def comments(post_id):
    if request.method == 'GET':
        try:
            with sqlite3.connect('reddit.db') as connection:
                connection.row_factory = dict_factory
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT * FROM comments WHERE comments.post_id = ?;
                    """, (post_id))
                comments = cursor.fetchall()
        except:
            result = {'status': 0, 'message': 'error'}
        return json.dumps(comments)
    elif request.method == 'POST':
        data = request.get_json(force=True)
        result = add_comment(data['content'], data['author'], post_id)
        return jsonify(result)
@application.route('/api/posts/<post_id>/comments/<comment_id>', methods = ['PATCH', 'DELETE'])
def comment(post_id, comment_id):
    if request.method == 'PATCH':
        data = request.get_json(force=True)
        result = edit_comment(data['content'], data['author'], data['id'])
        return jsonify(result)
    elif request.method == 'DELETE':
        try:
            with sqlite3.connect('reddit.db') as connection:
                cursor = connection.cursor()
                cursor.execute("""
                DELETE FROM comments WHERE id = ?;
                """, (comment_id,))
                result = cursor.fetchall()
        except:
            result = {'status': 0, 'message': 'error'}
        return jsonify(result)
#HELPER FUNCTIONS
def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
def add_post(title, body, author, image_url):
    try:
        with sqlite3.connect('reddit.db') as connection:
            # connection.row_factory = dict_factory
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO posts ( title, body, author, image_url, vote_count) values (?, ?, ?, ?, 0);
            """, ( title, body, author, image_url))
            result = cursor.fetchall()
    except:
        result = {'status': 0, 'message': 'error'}
        return result
def edit_post(title, body, author, image_url, postid):
    try:
        with sqlite3.connect('reddit.db') as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE posts SET title = ?, body = ?, author = ?, image_url = ? WHERE ID = ?;", (title, body, author, image_url, postid))
            result = cursor.fetchall()
    except:
        result = {'status': 0, 'message': 'Error'}
    return result
def add_comment(content, author, postid):
    try:
        with sqlite3.connect('reddit.db') as connection:
            # connection.row_factory = dict_factory
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO comments (content, author, post_id) values (?, ?, ?);
            """, (content, author, postid))
            result = cursor.fetchall()
    except:
        result = {'status': 0, 'message': 'error'}
        return result
def edit_comment(content, author, commentid):
    try:
        with sqlite3.connect('reddit.db') as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE comments SET content = ?, author = ? WHERE ID = ?;", (content, author, commentid))
            result = cursor.fetchall()
    except:
        result = {'status': 0, 'message': 'Error'}
    return result
# @application.route('/', methods=['GET', 'POST'])
# @application.route('/index', methods=['GET', 'POST'])
# def index():
#     form1 = EnterDBInfo(request.form)
#     form2 = RetrieveDBInfo(request.form)
#
#     if request.method == 'POST' and form1.validate():
#         data_entered = Data(notes=form1.dbNotes.data)
#         try:
#             db.session.add(data_entered)
#             db.session.commit()
#             db.session.close()
#         except:
#             db.session.rollback()
#         return render_template('thanks.html', notes=form1.dbNotes.data)
#
#     if request.method == 'POST' and form2.validate():
#         try:
#             num_return = int(form2.numRetrieve.data)
#             query_db = Data.query.order_by(Data.id.desc()).limit(num_return)
#             for q in query_db:
#                 print(q.notes)
#             db.session.close()
#         except:
#             db.session.rollback()
#         return render_template('results.html', results=query_db, num_return=num_return)
#
#     return render_template('index.html', form1=form1, form2=form2)

if __name__ == '__main__':
    application.run(host='0.0.0.0')
