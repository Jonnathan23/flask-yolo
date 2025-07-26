import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key')
    # Otros settings comunes

class DevConfig(Config):
    DEBUG = True
    # Configs de desarrollo

class ProdConfig(Config):
    DEBUG = False
    # Configs de producción
