from flask import Flask, url_for, redirect, request, render_template
from apps.book import bp as book_bp
from apps.course import bp as course_bp
from apps.user import bp as user_bp
import configparser
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import config

app = Flask(__name__)
app.config.from_object(config)

app.register_blueprint(course_bp)
app.register_blueprint(user_bp)

books = [
    {"id": 1, "name": "Hello"},
    {"id": 2, "name": "World"},
    {"id": 3, "name": "2022"},
]

db_config = configparser.ConfigParser()

db_config.read('db_config.ini')
db_dict = db_config['DB']
db_uri = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(db_dict['username'], db_dict['password'], db_dict['hostname'],
                                                 int(db_dict['port']), db_dict['database'])
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(32), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", backref="articles")

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False)

# with app.app_context():
#     db.create_all()


@app.route('/article')
def article_view():
    # CRUD

    # Create
    # article = Article(title="Paper 1", content="Recently...")
    # db.session.add(article)
    # db.session.commit()

    # Read
    # article = Article.query.filter_by(id=1)[0]
    # print(article.title)

    # Update
    article = Article.query.filter_by(id=1)[0]
    article.content = 'Oops'
    db.session.commit()

    # Delete
    Article.query.filter_by(id=1).delete()
    db.session.commit()
    return "success!"


@app.route('/book/list')
def book_list():
    for book in books:
        book["url"] = url_for("book_detail", book_id=book["id"])
    return books


@app.route('/book/<int:book_id>', methods=['GET'])
def book_detail(book_id):
    for book in books:
        if book["id"] == book_id:
            return book

    return f"No such books: {book_id}"


@app.route('/profile')
def profile():
    user_id = request.args.get("id")
    if user_id:
        return "Personal Centre"
    else:
        return redirect(url_for("index"))


@app.route('/about')
def about():
    context = {
        "username": "Jae"
    }
    return render_template("about.html", **context)


@app.route('/control')
def control():
    context = {
        "age": 17,
        "books": ["book1", "book2", "book3"],
        "people": {"jae": 24, "di": 18}
    }
    return render_template("control.html", **context)


@app.route('/')
def index():  # put application's code here
    engine = db.engine
    with engine.connect() as conn:
        result = conn.execute("select * from t02")
        print(result.fetchall())
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
