# -*- encoding: utf-8 -*-
from app.app import Flask


def register_blueprints(my_app):
    from app.api.v1 import create_blueprint_v1

    my_app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


def register_plugin(my_app):
    from app.models.base import db
    db.init_app(my_app)
    with my_app.app_context():
        db.create_all()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.conf.secure')
    app.config.from_object('app.conf.setting')

    register_blueprints(app)
    register_plugin(app)

    return app
