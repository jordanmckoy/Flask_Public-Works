from os import getenv
from flask_mail import Mail
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from dotenv import load_dotenv

db = SQLAlchemy()
login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('auth', 'employee', 'manager', 'user'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()
load_dotenv()
mail = Mail()
def create_app(config):
    app = Flask(__name__)
    app.config['MAIL_SERVER'] = getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = getenv('MAIL_PORT')
    app.config['MAIL_USERNAME'] = getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = getenv('MAIL_PASSWORD')

    app.config['MAIL_USE_SSL'] = getenv('MAIL_USE_SSL')
    mail.init_app(app)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app
