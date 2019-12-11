from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'asdf123cvxc'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/new-post', methods=['POST', 'GET'])
def new_post():

    title_error = ''
    body_error = ''

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        blog_post = Blog(title, body)
        db.session.add(blog_post)
        db.session.commit()

        if not title:
            title_error = "Input title"
            title = ''
        
        if not body:
            body_error = "Input body"
            body = ''

        if (title_error or body_error):
            return render_template('new-post.html', title_error=title_error, body_error=body_error)

        return render_template('viewpost.html', blog=blog_post)

    return render_template('new-post.html')

@app.route('/blog', methods=['GET'])
def blog():
    blog_id = request.args.get('id')
    if blog_id:
        blog = Blog.query.get(blog_id)
        return render_template('viewpost.html', blog=blog)
   
   
   
    blogs = Blog.query.all()
    return render_template("main-page.html", blogs=blogs)


if __name__ == '__main__':
    app.run()



