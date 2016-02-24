import os
import sys
import stat

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY_FILE = '/etc/secret.txt'

class Config(object):
    if os.path.isfile(SECRET_KEY_FILE):
        with open(SECRET_KEY_FILE) as f:
            SECRET_KEY = f.read().strip()
    else:
        sys.exit('ERROR: SECRET KEY not found, put it in {}'.format(SECRET_KEY_FILE))

    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    SQLITE_DB_FILE = os.path.join(BASE_DIR, 'prod_uncertaind.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + SQLITE_DB_FILE


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'uncertaind.db')
    DEBUG = True
    SQLALCHEMY_ECHO = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False