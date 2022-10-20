from flask import Blueprint

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/list")
def user_list():
    return "user list"
