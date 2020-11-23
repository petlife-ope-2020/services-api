from flask_restful import abort
from flask.json import jsonify

from services.utils.db.adapter_factory import get_mongo_adapter
from services.api.body_parsers.removal import RemovalParser


class RemovalService:
    """ For a petshop to remove itself from
        the providers list of a service,
        if the list becomes empty after the operation,
        the whole object is deleted, as there is
        no service if no one is providing it.

        Args:
            Gotten from the parser, service_id and petshop_username.

        Returns:
            updated_service (dict): The service without the sender as a provider
            205 (status): If the service is deleted after the operation.

        Raises:
            409 (status): If there are any errors with the operations on MongoDB.
    """
    def __init__(self):
        self.parser = RemovalParser()

    def remove(self):
        """ Parses the fields and calls the db methods.
        """
        doc = self.parser.fields
        updated_service = self._remove_from_mongo(doc)

        if not updated_service['available_in']:
            self._delete_service(updated_service['_id'])
            return 'No other providers, service deleted.', 205

        return jsonify(updated_service)

    @staticmethod
    def _remove_from_mongo(doc):
        mongo = get_mongo_adapter()
        try:
            return mongo.remove_self(doc)
        except KeyError as error:
            abort(409, extra=f'{error}')

    @staticmethod
    def _delete_service(doc_id):
        mongo = get_mongo_adapter()
        try:
            mongo.delete_service(doc_id)
        except KeyError as error:
            abort(409, extra=f'{error}')
