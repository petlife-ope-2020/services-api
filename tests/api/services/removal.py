import unittest
from unittest.mock import MagicMock, patch

from services.api.services.removal import RemovalService


# pylint: disable=protected-access
class RemovalServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.patches = []
        self.mocks = {}

        abort_patch = patch('services.api.services.removal.abort')
        self.mocks['abort_mock'] = abort_patch.start()
        self.patches.append(abort_patch)

        jsonify_patch = patch('services.api.services.removal.jsonify')
        self.mocks['jsonify_mock'] = jsonify_patch.start()
        self.patches.append(jsonify_patch)

        mongo_patch = patch('services.api.services.removal.get_mongo_adapter')
        self.mocks['mongo_mock'] = mongo_patch.start()
        self.patches.append(mongo_patch)

        parser_patch = patch('services.api.services.removal.RemovalParser')
        self.mocks['parser_mock'] = parser_patch.start()
        self.patches.append(parser_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_init_creates_parser(self):
        # Setup
        mock_self = MagicMock()

        # Act
        RemovalService.__init__(mock_self)

        # Assert
        self.mocks['parser_mock'].assert_called()

    def test_remove_return_updated_doc(self):
        # Setup
        mock_self = MagicMock()
        mock_self._remove_from_mongo.return_value = {
            'available_in': {
                'some': 'petshop'
            }
        }

        # Act
        RemovalService.remove(mock_self)

        # Assert
        self.mocks['jsonify_mock'].assert_called_with({
            'available_in': {
                'some': 'petshop'
            }
        })

    def test_remove_no_other_providers_returns_205(self):
        # Setup
        mock_self = MagicMock()
        mock_self._remove_from_mongo.return_value = {
            '_id': 'some_id',
            'available_in': {}
        }

        # Act
        response = RemovalService.remove(mock_self)

        # Assert
        mock_self._delete_service.assert_called()
        self.assertEqual(response, ('No other providers, service deleted.', 205))

    def test_remove_from_mongo_returns_mongo_call(self):
        # Setup
        doc = {}

        # Act
        RemovalService._remove_from_mongo(doc)

        # Assert
        self.mocks['mongo_mock'].return_value.remove_self.assert_called_with({})

    def test_remove_from_mongo_keyerror_abort(self):
        # Setup
        doc = {}
        self.mocks['mongo_mock'].return_value.remove_self.side_effect = \
            KeyError('No such object in collection')

        # Act
        RemovalService._remove_from_mongo(doc)

        # Assert
        self.mocks['abort_mock'].assert_called_with(
            409, extra="'No such object in collection'"
        )

    def test_delete_service_returns_mongo_call(self):
        # Setup
        doc = {}

        # Act
        RemovalService._delete_service(doc)

        # Assert
        self.mocks['mongo_mock'].return_value.delete_service.assert_called_with({})

    def test_delete_service_keyerror_abort(self):
        # Setup
        doc = {}
        self.mocks['mongo_mock'].return_value.delete_service.side_effect = \
            KeyError('No such object in collection')

        # Act
        RemovalService._delete_service(doc)

        # Assert
        self.mocks['abort_mock'].assert_called_with(
            409, extra="'No such object in collection'"
        )
