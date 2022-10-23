from flask import Blueprint, render_template
from exts import mail
from flask_mail import Message
from models import EmailCaptureModel

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route('/login')
def login():
    return render_template("login.html")


@bp.route('/register')
def register():
    return render_template("register.html")


@bp.route('/mail')
def my_mail():
    message = Message(
        subject='Test',
        recipients=['jl5999@columbia.edu'],
        body='This is a test email.'
    )
    mail.send(message)
    return "success"
