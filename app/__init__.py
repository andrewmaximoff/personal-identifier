import dropbox

from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment

from config import Config
from app.utils.http_errors import page_not_found, forbidden

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
moment = Moment()
dbx = dropbox.Dropbox(Config.DROPBOX_TOKEN)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.static_folder = 'static'
    app.add_url_rule('/static/<path:filename>',
                     endpoint='static',
                     view_func=app.send_static_file)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, forbidden)

    from .home import bp as home_bp
    app.register_blueprint(home_bp)

    from .profile import bp as profile_bp
    app.register_blueprint(profile_bp, url_prefix='/profile')

    from .api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app


@login.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))


from app import models
