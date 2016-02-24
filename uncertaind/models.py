import os
import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from uncertaind import app, db

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    log = db.Column(db.String(128), unique=True, nullable=True, default=None)

    def __init__(self, name, log):
        self.name = name
        self.log = log

    def __unicode__(self):
        return self.name


# Automatic database creation in production
# sqlite
if not app.config.get('DEBUG') and app.config.get('SQLITE_DB_FILE'):
    SQLITE_DB_FILE = app.config.get('SQLITE_DB_FILE')
    # Create the sqlite db file if it doesn't exist
    if not os.path.isfile(SQLITE_DB_FILE):
        import sqlite3

        sqlite3.connect(SQLITE_DB_FILE)
        os.chmod(SQLITE_DB_FILE, 0o777)
        db.create_all()