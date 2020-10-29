import unittest
from unittest.mock import patch

from services.utils.db.adapter_factory import get_mongo_adapter


class AdapterFactoryTestCase(unittest.TestCase):

    @staticmethod
    @patch('services.utils.db.adapter_factory.MongoAdapter')
    def test_get_mongo_adapter_first_call(mongo_mock):
        # Setup
        get_mongo_adapter.adapter = None

        # Act
        get_mongo_adapter()

        # Assert
        mongo_mock.assert_called()

    @staticmethod
    @patch('services.utils.db.adapter_factory.MongoAdapter')
    def test_get_mongo_adapter_subsequent_calls(mongo_mock):
        # Setup
        get_mongo_adapter.adapter = True

        # Act
        get_mongo_adapter()

        # Assert
        mongo_mock.assert_not_called()
