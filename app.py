from flask import Flask, url_for, redirect, request, render_template
from apps.book import bp as book_bp
from apps.course import bp as course_bp
from apps.user import bp as user_bp

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
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
