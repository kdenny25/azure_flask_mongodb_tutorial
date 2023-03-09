from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId

import datetime

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client.flask_db
blogs = db.blogs

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
