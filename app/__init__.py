from flask import Flask
from flask_jwt_extended import JWTManager
from flask_orator import Orator

from app.models.revoked_token import RevokedTokens
from config import config

db = Orator()
jwt = JWTManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    jwt.init_app(app)
    app.config['JWT_SECRET_KEY'] = '.g+8{7jnZ=Fhp(85V$Rx.'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    # This is where we import our routes
    from .routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokens.where('jti', jti).first()
