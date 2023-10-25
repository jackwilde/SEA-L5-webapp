from flask import Flask
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from app.auth import auth

BASEDIR = Path(__file__).parent
DB_NAME = "data.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "79zMopyNtucBbkv3Y3ZvFFHUnzJTVNHH"
app.register_blueprint(blueprint=auth, url_prefix="/")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BASEDIR}/{DB_NAME}"
db = SQLAlchemy(app)


