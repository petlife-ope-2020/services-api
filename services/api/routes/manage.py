from flask_restful import Resource

from services.api.services.creation import CreationService


class Manage(Resource):
    """ For a petshop to manage the services they provide."""

    @staticmethod
    def post():
        service = CreationService()
        return service.create()
