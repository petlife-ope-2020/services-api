from flask_restful import Resource

from services.api.services.search import SearchService


class Search(Resource):
    """ For a client to search for the available services."""

    @staticmethod
    def get():
        service = SearchService()
        return service.search()
