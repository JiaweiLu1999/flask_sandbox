from flask import Flask
from blueprints import qa_bp, user_bbp
import config
from exts import db

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

app.register_blueprint(qa_bp)
app.register_blueprint(user_bbp)

if __name__ == '__main__':
    app.run()
