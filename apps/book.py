from flask import Blueprint

bp = Blueprint("book", __name__, url_prefix="/book")


@bp.route("/list")
def book_list():
    return "book list"
