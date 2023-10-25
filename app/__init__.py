from flask import Flask
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from app.auth import auth
from app.models import db, User

BASEDIR = Path(__file__).parent
DB_NAME = "data.db"

def create_db(app, db):
    if not Path(f"{BASEDIR}/{DB_NAME}").exists():
        with app.app_context():
            db.create_all()


app = Flask(__name__)
app.config["SECRET_KEY"] = "79zMopyNtucBbkv3Y3ZvFFHUnzJTVNHH"
app.register_blueprint(blueprint=auth, url_prefix="/")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BASEDIR}/{DB_NAME}"

db.init_app(app)

create_db(app, db)

