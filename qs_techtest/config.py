import os


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY") or "ohsosecret"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")


class Testing(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
