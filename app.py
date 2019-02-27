from flask import Flask, request, render_template,\
                  redirect, url_for, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)

db_uri = "sqlite:///test.db"
# db_uri = os.environ.get('DATABASE_URL') #or "postgresql://localhost/flasknote"
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["DEBUG"] = True
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    article = db.Column(db.Text())
    pub_date = db.Column(db.DateTime, nullable=False,
                                default=datetime.utcnow)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    thread = db.relationship('Thread',
        backref=db.backref('articles', lazy=True))

    def __repr__(self):
        return '<Article %r>' % self.name

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    threadname = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Thread %r>' % self.threadname


@app.route("/")
def index():
    threads = Thread.query.all()
    return render_template("index.html", threads=threads)

@app.route("/thread/<title>/")
def thread_detail_show(title):
    title = Thread.query.filter_by(threadname=title).first()
    articles = Article.query.filter_by(thread_id=title.id).all()
    return render_template('thread.html',
                            thread=title.threadname,
                            articles=articles)

@app.route("/result", methods=["POST"])
def article_add():
    res = request.form
    thread = Thread.query.filter_by(threadname=res["thread"]).first()
    data = Article(name=res["name"],
                   article=res["article"],
                   thread_id=thread.id)
    db.session.add(data)
    db.session.commit()
    return redirect(url_for('thread_detail_show', title=res["thread"]))

@app.route("/create", methods=["POST"])
def thread_create():
    thread_get = request.form["thread"]
    thread_list = []
    threads = Thread.query.all()
    thread_list = [th.threadname for th in threads]
    if thread_get not in thread_list:
        thread_new = Thread(threadname=thread_get)
        db.session.add(thread_new)
        db.session.commit()
    return redirect(url_for('thread_detail_show', title=thread_get))

@app.route("/api_get/<key>", methods=["GET"])
def api_get(key):
    data = {key: []}
    thread_api_get = Thread.query.filter_by(threadname=key).first()
    articles = Article.query.filter_by(thread_id=thread_api_get.id).all()
    for article in articles:
        r = {"name": article.name, "article": article.article}
        data[key].append(r)
    return jsonify(data)

@app.route("/api_post", methods=["POST"])
def api_post():
    print(request.data)
    api_data_post = request.data.decode()
    data = {api_data_post: []}
    print(api_data_post)
    thread_api_get = Thread.query.filter_by(threadname=api_data_post).first()
    articles = Article.query.filter_by(thread_id=thread_api_get.id).all()
    for article in articles:
        r = {"name": article.name, "article": article.article}
        data[api_data_post].append(r)
    return jsonify(data)

if __name__ == "__main__":
    app.run()