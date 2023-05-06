import os
import logging

# Configuración base
class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-por-defecto'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Configuración para Flask-RESTful
    RESTFUL_JSON = {'indent': 4}

# Configuración para producción
class ProductionConfig(Config):
    DEBUG = False

# Configuración para entorno de desarrollo
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

# Configuración para entorno de pruebas
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite3'

# Seleccionar la configuración dependiendo del entorno
app_config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
