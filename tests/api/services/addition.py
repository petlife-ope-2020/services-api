import unittest
from unittest.mock import MagicMock, patch

from services.api.services.addition import AdditionService


# pylint: disable=protected-access
class AdditionServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.patches = []
        self.mocks = {}

        abort_patch = patch('services.api.services.addition.abort')
        self.mocks['abort_mock'] = abort_patch.start()
        self.patches.append(abort_patch)

        jsonify_patch = patch('services.api.services.addition.jsonify')
        self.mocks['jsonify_mock'] = jsonify_patch.start()
        self.patches.append(jsonify_patch)

        mongo_patch = patch('services.api.services.addition.get_mongo_adapter')
        self.mocks['mongo_mock'] = mongo_patch.start()
        self.patches.append(mongo_patch)

        parser_patch = patch('services.api.services.addition.AdditionParser')
        self.mocks['parser_mock'] = parser_patch.start()
        self.patches.append(parser_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_init_creates_parser(self):
        # Setup
        mock_self = MagicMock()

        # Act
        AdditionService.__init__(mock_self)

        # Assert
        self.mocks['parser_mock'].assert_called()

    def test_create_calls_methods_return_json_response(self):
        # Setup
        mock_self = MagicMock(
            parser=MagicMock(
                fields={
                    'petshop_username': 'test123',
                    'petshop_name': 'test123',
                    'service_id': '123'
                }
            )
        )

        # Act
        AdditionService.add(mock_self)

        # Assert
        mock_self._resolve_fields_to_db_object.assert_called_with({
            'petshop_username': 'test123',
            'petshop_name': 'test123',
            'service_id': '123'
        })
        mock_self._insert_in_mongo.assert_called_with({
            'petshop_username': 'test123',
            'petshop_name': 'test123',
            'service_id': '123'
        })
        self.mocks['jsonify_mock'].assert_called()

    def test_resolve_fields_to_db_object_alters_doc(self):
        # Setup
        doc = {
            'petshop_username': 'test_user',
            'petshop_name': 'test_name'
        }

        # Act
        AdditionService._resolve_fields_to_db_object(doc)

        # Assert
        self.assertEqual(doc, {
            'available_in': {
                'petshop_username': 'test_user',
                'petshop_name': 'test_name'
            }
        })

    def test_insert_in_mongo_returns_add_method(self):
        # Setup
        doc = {}

        # Act
        result = AdditionService._insert_in_mongo(doc)

        # Assert
        self.assertEqual(
            result,
            self.mocks['mongo_mock'].return_value.add_self.return_value
        )

    def test_insert_in_mongo_keyerror_calls_abort(self):
        # Setup
        doc = {}
        self.mocks['mongo_mock'].return_value.\
            add_self.side_effect = KeyError('No such object in collection')

        # Act
        AdditionService._insert_in_mongo(doc)

        # Assert
        self.mocks['abort_mock'].assert_called_with(
            409, extra="'No such object in collection'"
        )
