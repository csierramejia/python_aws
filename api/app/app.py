from flask import Flask
from flask_cors import CORS
from blueprints import (
    rekognition,
    sns
)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.register_blueprint(rekognition.bp)
    app.register_blueprint(sns.bp)

    return app
