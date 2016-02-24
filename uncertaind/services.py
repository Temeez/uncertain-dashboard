import os
import subprocess
from datetime import datetime, timedelta
from systemd.manager import Manager as Systemd_Manager
from sqlalchemy import asc

from uncertaind import db
from uncertaind.models import Service

sys_manager = Systemd_Manager()

class Services():
    def service_data(self, name, log=None):
        try:
            unit = sys_manager.get_unit(name)
        except Exception as e:
            return {
                'result': False,
                'reason': str(e)
            }, 404

        now = datetime.now()
        active_time = datetime.fromtimestamp(unit.properties.ActiveEnterTimestamp / 1000000)
        inactive_time = datetime.fromtimestamp(unit.properties.InactiveEnterTimestamp / 1000000)
        active_ago = now - active_time
        inactive_ago = now - inactive_time

        if ('-1' in str(inactive_ago)):
            inactive_ago = now - now

        dict = {}

        if log:
            dict.update({
                'log': self.get_service_log(log),
                'logfile': log
            })

        dict.update({
            'service': name,
            'Id': str(unit.properties.Id),
            'Description': str(unit.properties.Description),
            'FragmentPath': str(unit.properties.FragmentPath),
            'LoadState': str(unit.properties.LoadState),
            'ActiveState': str(unit.properties.ActiveState),
            'SubState': str(unit.properties.SubState),
            'ActiveTime': str(active_ago).split('.')[0],
            'InactiveTime': str(inactive_ago).split('.')[0]
        })

        return dict


    def get_services(self):
        services = []
        list = []

        try:
            services = Service.query.order_by(asc(Service.name)).all()
        except Exception as e:
            return {
                'result': False,
                'reason': str(e)
            }, 404
        for service in services:
            list.append(self.service_data(service.name, service.log))
        return list


    def get_service(self, name):
        return self.service_data(name)


    def get_service_log(self, log, lines=30):
        list = []
        if os.path.isfile(log):
            p = subprocess.Popen(['tail', '-n', str(lines), log], stdout=subprocess.PIPE)
            soutput, sinput = p.communicate()
            for line in soutput.splitlines():
                list.append(line.decode())
        return list


    def add_service(self, name, log=None):
        unit = None
        try:
            unit = sys_manager.get_unit(name)
        except Exception as e:
            return {
                'result': False,
                'reason': str(e)
            }, 404
        if unit:
            try:
                db.session.add(Service(name, log))
                db.session.commit()
            except Exception as e:
                return {
                    'result': False,
                    'reason': str(e)
                }, 500
            return { 'result': True }, 201
        return {
            'result': False,
            'reason': 'Unknown'
        }, 500


    def edit_service(self, name, log):
        try:
            s = Service.query.filter_by(name=name).first()
            s.name = name
            s.log = log
            db.session.commit()
        except Exception as e:
            return {
                'result': False,
                'reason': str(e)
            }, 304
        return { 'result': True }, 200


    def remove_service(self, name):
        try:
            result = Service.query.filter_by(name=name).delete()
            if result == 1:
                db.session.commit()
                return { 'result': True }, 200
            else:
                return {
                    'result': False,
                    'reason': 'Service not found'
                }, 404
        except Exception as e:
            return {
                'result': False,
                'reason': str(e)
            }, 304
        return {
            'result': False,
            'reason': 'Unknown.'
        }, 500


    def restart_service(self, name):
        try:
            unit = sys_manager.get_unit(name).restart('fail')
        except Exception as e:
            return {
                'result': False,
                'reason': str(e)
            }, 404
        return { 'result': True }, 200


    def stop_service(self, name):
        try:
            unit = sys_manager.get_unit(name).stop('fail')
        except Exception as e:
            return {
                'result': False,
                'reason': str(e)
            }, 404
        return { 'result': True }, 200


    def start_service(self, name):
        try:
            unit = sys_manager.get_unit(name).start('fail')
        except Exception as e:
            return {
                'result': False,
                'reason': str(e)
            }, 404
        return { 'result': True }, 200