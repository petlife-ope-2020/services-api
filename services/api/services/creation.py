import re

from flask_restful import abort
from flask.json import jsonify

from services.utils.db.adapter_factory import get_mongo_adapter
from services.api.body_parsers.creation import CreationParser


class CreationService:
    """ Service for creating a service object.
        This will be called when a shop wants to provide a service
        that none other provide yet.

        Args:
            service_name (str): This will be sent on the POST form
                                and must not match any special characters.
    """
    def __init__(self):
        self.parser = CreationParser()

    def create(self):
        """ Gets the field and validates its value,
            sending it to MongoDB if value is approved.

            Returns
                new_service_id (str): The created service's id
        """
        doc = self.parser.field
        self._check_naming_pattern(doc['service_name'])
        new_service_id = self._insert_in_mongo(doc)
        return jsonify(new_service_id)

    @staticmethod
    def _check_naming_pattern(user_input):
        if not re.match(r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]*$', user_input):
            abort(403, extra='Invalid service name.')

    @staticmethod
    def _insert_in_mongo(doc):
        mongo = get_mongo_adapter()
        try:
            return mongo.create(doc)
        except KeyError as error:
            abort(409, extra=f'{error}')
