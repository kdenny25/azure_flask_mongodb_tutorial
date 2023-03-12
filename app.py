import os

from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId
import os, sys

import datetime

app = Flask(__name__)

print(os.environ)

# if 'WEBSITE_HOSTNAME' not in os.environ:
#     # local development
#     client = MongoClient('localhost', 27017)
# else:
#     # production
#     print('Loading config.production.')
#     conn_str = os.environ.get('AZURE_COSMOS_CONNECTIONSTRING')
#     client = MongoClient(conn_str)

# must add new application setting with read-write connection string
# connection string is copied from the database connection strings menu.
conn_str = os.environ.get('COSMOS_CONNECTION_STRING')
client = MongoClient(conn_str)

db = client.flask_db
blogs = db.blogs
s
@app.route('/', methods=['GET', 'POST'])
def index():  # put application's code here
    all_blogs = blogs.find()
    return render_template('index.html', blogs=all_blogs)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        # each blog post should have a date created
        date = datetime.datetime.now()
        title = request.form['blogTitle']
        content = request.form['blogContent']
        blogs.insert_one({'date': date, 'title': title, 'content': content})

        return render_template('new_post.html', alert={'visibility': 'visible', 'message':'Post successfully submitted!!'})
    else:
        return render_template('new_post.html', alert={'visibility': 'hidden', 'message':''})

@app.post('/<id>')
def read_post(id):
    blog_post = blogs.find_one({'_id': ObjectId(id)})
    return render_template('read_post.html', blog=blog_post)

if __name__ == '__main__':
    app.run()
