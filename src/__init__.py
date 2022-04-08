import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.database import db
from src.authenticate import authenticate
from src.account_balance_inquiry import account_balance_inquiry
from src.mini_statement import mini_statement
from src.funds_transfer import funds_transfer
from src.title_fetch import title_fetch
from src.ibft import ibft
from src.bill_inquiry import bill_inquiry
from src.bill_payment import bill_payment
from src.config.swagger import template, swagger_config
from flasgger import Swagger

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
            SWAGGER={
                'title': "API POMFB",
                'uiversion': 3
            }
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)

    JWTManager(app)
    app.register_blueprint(authenticate)
    app.register_blueprint(account_balance_inquiry)
    app.register_blueprint(mini_statement)
    app.register_blueprint(funds_transfer)
    app.register_blueprint(title_fetch)
    app.register_blueprint(ibft)
    app.register_blueprint(bill_inquiry)
    app.register_blueprint(bill_payment)

    Swagger(app, config=swagger_config, template=template)

    @app.get("/hello")
    def say_hello():
        return {"message": "Hello world"}

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong, we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR

    return app