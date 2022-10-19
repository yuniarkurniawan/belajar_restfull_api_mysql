class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "my-secret-key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = "my-secret-password"
    MAIL_DEFAULT_SENDER = 'your_email'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'your_email'
    MAIL_PASSWORD = 'your_password'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI =  \
        "postgresql+psycopg2://root:"\
        "<password>@localhost:5432"\
        "/blablu"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI =  \
        "postgresql+psycopg2://root:"\
        "<password>@localhost:5432"\
        "/blablu"
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = True
    JWT_SECRET_KEY = 'JWT-SECRET'
    SECRET_KEY = 'my-secret-key'
    SECURITY_PASSWORD_SALT = 'my-secret-password'
    MAIL_DEFAULT_SENDER = 'your_email'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = "your_email"
    MAIL_PASSWORD = "your_password"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
