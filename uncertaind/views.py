import os

from flask import render_template, redirect, request, flash, g, session, url_for
from sqlalchemy import asc

from uncertaind import app, db
from uncertaind.models import Service
from uncertaind.disks import Disks
from uncertaind.services import Services

disks = Disks()
services = Services()

@app.route('/')
def index():
    disk_list = disks.get_disks()
    disk_smart = disks.SMART.get_data()
    service_list = services.get_services()

    return render_template('index.html', disks=disk_list, smart=disk_smart, services=service_list)


@app.route('/add', methods=['POST'])
def service_add():
    name = request.form['service']
    log = request.form['log'] or None

    services.add_service(name, log)
    return redirect(url_for('index'))


@app.route('/edit', methods=['POST'])
def service_edit():
    name = request.form['service']
    log = request.form['log'] or None

    services.edit_service(name, log)
    return redirect(url_for('index'))


@app.route('/remove/<name>')
def service_remove(name):
    services.remove_service(name)
    return redirect(url_for('index'))


@app.route('/restart/<name>')
def service_restart(name):
    services.restart_service(name)
    return redirect(url_for('index'))


@app.route('/stop/<name>')
def service_stop(name):
    services.stop_service(name)
    return redirect(url_for('index'))


@app.route('/start/<name>')
def service_start(name):
    services.start_service(name)
    return redirect(url_for('index'))