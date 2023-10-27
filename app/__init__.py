from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.auth import auth
from app.models import db, User
from app.views import views

MYSQL_USER = ""
MYSQL_PASSWORD = ""
MYSQL_SERVER = ""
MYSQL_DB = ""

app = Flask(__name__)
app.config["SECRET_KEY"] = "79zMopyNtucBbkv3Y3ZvFFHUnzJTVNHH"
app.register_blueprint(blueprint=auth, url_prefix="/")
app.register_blueprint(blueprint=views, url_prefix="/")

app.config["SQLALCHEMY_DATABASE_URI"] = \
    f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}/{MYSQL_DB}"

db.init_app(app)

# create_db(app, db)
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = "auth.sign_in"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))