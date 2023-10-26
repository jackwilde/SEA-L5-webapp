from flask import Flask
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.auth import auth
from app.models import db, User
from app.views import views

BASEDIR = Path(__file__).parent
DB_NAME = "data.db"

def create_db(app, db):
    if not Path(f"{BASEDIR}/{DB_NAME}").exists():
        with app.app_context():
            db.create_all()


app = Flask(__name__)
app.config["SECRET_KEY"] = "79zMopyNtucBbkv3Y3ZvFFHUnzJTVNHH"
app.register_blueprint(blueprint=auth, url_prefix="/")
app.register_blueprint(blueprint=views, url_prefix="/")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BASEDIR}/{DB_NAME}"

db.init_app(app)

create_db(app, db)

login_manager = LoginManager()
login_manager.login_view = "auth.sign_in"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))