import unittest
from unittest.mock import MagicMock, patch

from services.api.services.creation import CreationService


# pylint: disable=protected-access
class CreationServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.patches = []
        self.mocks = {}

        regex_patch = patch('services.api.services.creation.re')
        self.mocks['regex_mock'] = regex_patch.start()
        self.patches.append(regex_patch)

        abort_patch = patch('services.api.services.creation.abort')
        self.mocks['abort_mock'] = abort_patch.start()
        self.patches.append(abort_patch)

        jsonify_patch = patch('services.api.services.creation.jsonify')
        self.mocks['jsonify_mock'] = jsonify_patch.start()
        self.patches.append(jsonify_patch)

        mongo_patch = patch('services.api.services.creation.get_mongo_adapter')
        self.mocks['mongo_mock'] = mongo_patch.start()
        self.patches.append(mongo_patch)

        parser_patch = patch('services.api.services.creation.CreationParser')
        self.mocks['parser_mock'] = parser_patch.start()
        self.patches.append(parser_patch)

        mk_ngrams_patch = patch('services.api.services.creation.make_ngrams')
        self.mocks['mk_ngrams_mock'] = mk_ngrams_patch.start()
        self.patches.append(mk_ngrams_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_init_creates_parser(self):
        # Setup
        mock_self = MagicMock()

        # Act
        CreationService.__init__(mock_self)

        # Assert
        self.mocks['parser_mock'].assert_called()

    def test_create_calls_methods_return_json_response(self):
        # Setup
        mock_self = MagicMock(
            parser=MagicMock(field={'service_name': 'test123'})
        )
        self.mocks['mk_ngrams_mock'].return_value = 'hey'

        # Act
        CreationService.create(mock_self)

        # Assert
        mock_self._check_naming_pattern.assert_called_with(
            'test123'
        )
        mock_self._insert_in_mongo.assert_called_with({
            'service_name': 'test123', 'ngrams': 'hey'
        })
        self.mocks['jsonify_mock'].assert_called()

    def test_check_naming_pattern_no_match_abort(self):
        # Setup
        input_ = 'test_input'
        self.mocks['regex_mock'].match.return_value = None

        # Act
        CreationService._check_naming_pattern(input_)

        # Assert
        self.mocks['abort_mock'].assert_called_with(
            403, extra='Invalid service name.'
        )

    def test_insert_in_mongo_returns_create_method(self):
        # Setup
        doc = {}

        # Act
        result = CreationService._insert_in_mongo(doc)

        # Assert
        self.assertEqual(
            result,
            self.mocks['mongo_mock'].return_value.create.return_value
        )

    def test_insert_in_mongo_keyerror_calls_abort(self):
        # Setup
        doc = {}
        self.mocks['mongo_mock'].return_value.\
            create.side_effect = KeyError('Service already exists.')

        # Act
        CreationService._insert_in_mongo(doc)

        # Assert
        self.mocks['abort_mock'].assert_called_with(
            409, extra="'Service already exists.'"
        )
