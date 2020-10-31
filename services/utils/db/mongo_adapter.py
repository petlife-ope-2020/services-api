from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
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

    def add_self(self, doc):
        """ Adds a petshop as a provider of a service

            Args:
                doc (dict): The new petshop object to be appended

            Raises:
                KeyError: If the service_id is incorrect
                RuntimeError: If an unexpected error occurs

            Returns:
                updated_doc (dict): Service object with updated values
        """
        filter_ = {'_id': ObjectId(doc['service_id'])}
        del doc['service_id']
        try:
            updated_doc = self.db_.find_one_and_update(
                filter_,
                {'$push': doc},
                return_document=ReturnDocument.AFTER
            )
            if not updated_doc:
                raise KeyError('No such object in collection')

            updated_doc['_id'] = str(updated_doc['_id'])
            return updated_doc

        except PyMongoError as error:
            print(f'Error when performing update on MongoDB: {error}')
            raise RuntimeError from error

    def remove_self(self, doc):
        """ Removes a petshop as a provider of a service

            Args:
                doc (dict): The petshop object to be deleted

            Raises:
                KeyError: If the service_id is incorrect
                RuntimeError: If an unexpected error occurs

            Returns:
                updated_doc (dict): Service object without sender as a provider
        """
        filter_ = {'_id': ObjectId(doc['service_id'])}
        del doc['service_id']
        try:
            updated_doc = self.db_.find_one_and_update(
                filter_,
                {'$pull':{
                    'available_in': {
                        'petshop_username': doc['petshop_username']
                    }
                }},
                return_document=ReturnDocument.AFTER
            )
            if not updated_doc:
                raise KeyError('No such object in collection')

            updated_doc['_id'] = str(updated_doc['_id'])
            return updated_doc

        except PyMongoError as error:
            print(f'Error when performing update on MongoDB: {error}')
            raise RuntimeError from error

    def delete_service(self, doc_id):
        """ Deletes a service in the collection

            Args:
                doc_id (str): The id of the service to be deleted

            Raises:
                KeyError: If the service_id is incorrect
                RuntimeError: If an unexpected error occurs
        """
        filter_ = {'_id': ObjectId(doc_id)}
        try:
            deleted = self.db_.delete_one(filter_)

            if deleted.deleted_count == 0:
                raise KeyError('No such object in collection.')

        except PyMongoError as error:
            print(f'Error when performing deletion on MongoDB: {error}')
            raise RuntimeError from error
