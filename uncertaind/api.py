import os
import json

from flask_restful import Resource, Api

from uncertaind import app
from uncertaind.models import Service
from uncertaind.disks import Disks
from uncertaind.services import Services

api = Api(app)
disks = Disks()
services = Services()

class Service(Resource):
    def get(self, name):
        if name == 'all':
            return services.get_services()
        elif name:
            return services.get_service(name)

    def put(self, name):
        return services.add_service(name)

    def delete(self, name):
        return services.remove_service(name)

api.add_resource(Service, '/api/service/<string:name>')


class Disks(Resource):
    def get(self, name):
        if name == 'all' or not name:
            return disks.get_disks(), 200
        elif name == 'all+smart':
            return {
                'disks': disks.get_disks(),
                'smart': disks.SMART.get_data()
            }, 200
        elif name and '+smart' in name:
            arg = name.split('+')
            return {
                'disk': disks.get_disks(device=arg[0]),
                'smart': disks.SMART.get_data(device='/dev/{}'.format(arg[0]))
            }, 200
        elif name == '+smart':
            return {
                'result': 404,
                'reason': 'Erronous api call'
            }, 404
        elif name:
            list = disks.get_disks(device=name)
            if 404 in list:
                return list
            else:
                return list, 200

api.add_resource(Disks, '/api/disk/<string:name>')