import os
from decouple import config

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = config(
        'SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['cookies']


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "dev.db")
    SQLALCHEMY_ECHO = config('SQLALCHEMY_ECHO', cast=bool)


class ProdConfig:
    pass


class TestConfig:
    pass
