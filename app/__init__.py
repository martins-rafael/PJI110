import os

from flask import Flask
from flask_migrate import Migrate

from app.models import Member, init_defaults


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from . import models
    models.db.init_app(app)
    migrate = Migrate(app, models.db)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import main
    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='index')

    @app.before_first_request
    def create_tables():
        init_defaults()

    return app
