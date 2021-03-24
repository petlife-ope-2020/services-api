from flask_restful import abort
from flask.json import jsonify

from services.utils.db.adapter_factory import get_mongo_adapter
from services.api.body_parsers.addition import AdditionParser


# pylint: disable=inconsistent-return-statements
class AdditionService:
    """ Service for a shop to add itself as a provider of a listed service.
    """
    def __init__(self):
        self.parser = AdditionParser()

    def add(self):
        """ Gets the fields with the parser and
            resolves them into an object to be appended on the list
            of providers for the chosen service.

            Returns
                updated_service (object): The updated service with the new provider
        """
        doc = self.parser.fields
        self._resolve_fields_to_db_object(doc)
        updated_service = self._insert_in_mongo(doc)
        return jsonify(updated_service)

    @staticmethod
    def _insert_in_mongo(doc):
        mongo = get_mongo_adapter()
        try:
            return mongo.add_self(doc)
        except KeyError as error:
            abort(409, extra=f'{error}')

    @staticmethod
    def _resolve_fields_to_db_object(doc):
        doc['available_in'] = {
            'petshop_username': doc['petshop_username'],
            'petshop_name': doc['petshop_name']
        }
        del doc['petshop_username']
        del doc['petshop_name']
