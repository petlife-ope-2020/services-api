from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, PyMongoError

from services.utils.env_vars import MONGO_CONNECTION_STRING, SERVICES_COLLECTION


class MongoAdapter:
    """ Wrapper for connecting with Mongo DB and doing operations.
    """
    def __init__(self):
        self.client = MongoClient(
            MONGO_CONNECTION_STRING,
            connect=True
        )
        self.db_ = self.client.petlife[SERVICES_COLLECTION]

    def create(self, doc):
        """ Creates a document on set collection

            Args:
                doc (dict): The document being inserted

            Raises:
                KeyError: When document is duplicate

            Returns:
                new_service.inserted_id (str)
        """
        try:
            new_service = self.db_.insert_one(doc)
            return str(new_service.inserted_id)

        except DuplicateKeyError as error:
            raise KeyError('Service already exists.') from error

        except PyMongoError as error:
            raise RuntimeError('Unexpected error when working with MongoDB.') from error
