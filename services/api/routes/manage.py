from flask_restful import Resource

from services.api.services.creation import CreationService
from services.api.services.addition import AdditionService
from services.api.services.removal import RemovalService


class Manage(Resource):
    """ For a petshop to manage the services they provide."""

    @staticmethod
    def post():
        service = CreationService()
        return service.create()

    @staticmethod
    def put():
        service = AdditionService()
        return service.add()

    @staticmethod
    def delete():
        service = RemovalService()
        return service.remove()
