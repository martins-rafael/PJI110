import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate

from app.models import db, init_defaults

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL'),
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

    from . import announcements
    app.register_blueprint(announcements.bp)

    dev_mode = os.getenv('DEBUG')

    if dev_mode:
        @app.before_first_request
        def create_tables():
            db.create_all()
            init_defaults()

    return app
