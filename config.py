import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    ORATOR_DATABASES = {
        'default': 'mysql',
        'mysql': {
            'driver': 'mysql',
            'host': 'localhost',
            'database': 'flask_skeleton_2',
            'user': 'root',
            'password': 'munangwe22',
            'prefix': ''
        }
    }
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bmlnZ2FzaW5wYXJpcw=='


class TestingConfig(Config):
    Testing = True


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
