import os
import sys
import platform

if sys.version_info < (3, 3):
    sys.exit('ERROR: Python 3.3 or higher required, but found {}.'.format(platform.python_version()))

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object('config.ProdConfig')
db = SQLAlchemy(app)

try:
    from flask_debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension(app)
except:
    pass

from . import models, views, api

__version__ = '0.9.0'