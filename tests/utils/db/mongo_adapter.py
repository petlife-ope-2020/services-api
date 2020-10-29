import unittest
from unittest.mock import MagicMock, patch

from services.utils.db.mongo_adapter import MongoAdapter, DuplicateKeyError, PyMongoError


# pylint: disable=protected-access
class MongoAdapterTestCase(unittest.TestCase):

    def setUp(self):
        self.patches = []
        self.mocks = {}

        mongo_client_patch = patch('services.utils.db.mongo_adapter.MongoClient')
        self.mocks['mongo_client_mock'] = mongo_client_patch.start()
        self.patches.append(mongo_client_patch)

        mongo_conn_patch = patch('services.utils.db.mongo_adapter.MONGO_CONNECTION_STRING',
                                 new='test_conn_string')
        self.mocks['mongo_conn_mock'] = mongo_conn_patch.start()
        self.patches.append(mongo_conn_patch)

        services_col_patch = patch('services.utils.db.mongo_adapter.SERVICES_COLLECTION',
                                   new='test_services_string')
        self.mocks['services_col_mock'] = services_col_patch.start()
        self.patches.append(services_col_patch)

        return_doc_patch = patch('services.utils.db.mongo_adapter.ReturnDocument')
        self.mocks['return_doc_mock'] = return_doc_patch.start()
        self.patches.append(return_doc_patch)

        object_id_patch = patch('services.utils.db.mongo_adapter.ObjectId')
        self.mocks['object_id_mock'] = object_id_patch.start()
        self.patches.append(object_id_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_init_creates_client(self):
        # Setup
        mock_self = MagicMock()

        #  Act
        MongoAdapter.__init__(mock_self)

        # Assert
        self.mocks['mongo_client_mock'].assert_called_with(
            'test_conn_string',
            connect=True
        )
        self.assertEqual(
            mock_self.db_,
            self.mocks['mongo_client_mock'].return_value.petlife['test_services_string']
        )

    def test_create_successful_run_returns_inserted_id(self):
        # Setup
        mock_self = MagicMock()
        mock_self.db_.insert_one.return_value = MagicMock(inserted_id='new_id')
        doc = {}

        # Act
        new_service_id = MongoAdapter.create(mock_self, doc)

        # Assert
        self.assertEqual(new_service_id, 'new_id')

    def test_create_duplicated_entry_raises_key_error(self):
        # Setup
        mock_self = MagicMock()
        mock_self.db_.insert_one.side_effect = DuplicateKeyError(MagicMock())
        doc = {}

        # Act & Assert
        with self.assertRaises(KeyError):
            MongoAdapter.create(mock_self, doc)

    def test_create_unexpected_error_raises_runtime_error(self):
        # Setup
        mock_self = MagicMock()
        mock_self.db_.insert_one.side_effect = PyMongoError
        doc = {}

        # Act & Assert
        with self.assertRaises(RuntimeError):
            MongoAdapter.create(mock_self, doc)

    def test_add_self_not_updated_raises_key_error(self):
        # Setup
        mock_self = MagicMock()
        mock_self.db_.find_one_and_update.return_value = None
        doc = {'service_id': 'test_id'}

        # Act & Assert
        with self.assertRaises(KeyError):
            MongoAdapter.add_self(mock_self, doc)

    def test_add_self_updated_returns_updated_doc(self):
        # Setup
        mock_self = MagicMock()
        doc = {'service_id': 'test_id'}
        mock_self.db_.find_one_and_update.return_value = \
            {'_id': 'test_id'}

        # Act
        result = MongoAdapter.add_self(mock_self, doc)

        # Assert
        self.assertEqual(result, {'_id': 'test_id'})

    def test_add_self_unexpected_error_raises_runtime_error(self):
        # Setup
        mock_self = MagicMock()
        mock_self.db_.find_one_and_update.side_effect = PyMongoError
        doc = {'service_id': 'test_id'}

        # Act & Assert
        with self.assertRaises(RuntimeError):
            MongoAdapter.add_self(mock_self, doc)