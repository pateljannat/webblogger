from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI =  "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="jannatpatel",
    password="webblogger",
    hostname="jannatpatel.mysql.pythonanywhere-services.com",
    databasename="jannatpatel$posts",
)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default= "Anonymous")
    date_created = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)

    def __repr__(self):
        return "Blog Post" + str(self.id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts', methods=["GET", "POST"])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_created).all()
        return render_template('posts.html', posts=all_posts)


@app.route('/posts/read/<int:id>')
def read(id):
    post = BlogPost.query.get_or_404(id)
    return render_template('displayPost.html', post=post)

@app.route('/posts/delete/<int:id>')
def delete(id):
    postid = BlogPost.query.get_or_404(id)
    db.session.delete(postid)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    post = BlogPost.query.get_or_404(id)

    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        post.author = request.form["author"]
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

@app.route('/posts/create', methods=["GET", "POST"])
def create():
    if request.method == "POST":
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('create.html')
