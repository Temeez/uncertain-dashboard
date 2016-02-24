#!/usr/bin/env python
import os
from flask.ext.script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

from uncertaind import app
from uncertaind.models import db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('shell', Shell())
manager.add_command('db', MigrateCommand)

@manager.command
def db_create():
    db.create_all()

if __name__ == "__main__":
    if os.geteuid() != 0:
        print('WARNING: Not run as root! Some features will not work without root access!')
    manager.run()