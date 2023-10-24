from flask import Flask
from blueprints import blueprints

app = Flask(__name__)
app.config["SECRET_KEY"] = "79zMopyNtucBbkv3Y3ZvFFHUnzJTVNHH"
app.register_blueprint(blueprint=blueprints,
                       url_prefix="/")



if __name__ == '__main__':
    app.run()
