from flask import Flask
from blueprints import (
    rekognition,
    sns
)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(rekognition.bp)
    app.register_blueprint(sns.bp)

    return app
