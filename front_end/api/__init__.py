from flask import Flask
#from authlib.integrations.flask_client import OAuth
#for oauth

from front_end.api.blueprints.main import main_bp
from front_end.api.blueprints.admin import admin_bp
from front_end.api.blueprints.user import user_bp
from front_end.api.blueprints.auth import auth_bp


def create_app(config_name=None):
    app = Flask('api')

    # for now
    app.secret_key = 'secret something'
    app.config['SESSION_COOKIE_NAME'] = 'bill test cookie'
    # oauth = OAuth(app)



    register_blueprints(app)
    return app

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, prefix='/admin')
    app.register_blueprint(auth_bp, prefix='/auth')
    app.register_blueprint(user_bp, prefix='/user')