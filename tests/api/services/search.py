import unittest
from unittest.mock import MagicMock, patch

from services.api.services.search import SearchService


# pylint: disable=protected-access
class SearchServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.patches = []
        self.mocks = {}

        regex_patch = patch('services.api.services.search.re')
        self.mocks['regex_mock'] = regex_patch.start()
        self.patches.append(regex_patch)

        abort_patch = patch('services.api.services.search.abort')
        self.mocks['abort_mock'] = abort_patch.start()
        self.patches.append(abort_patch)

        mk_ngrams_patch = patch('services.api.services.search.make_ngrams')
        self.mocks['mk_ngrams_mock'] = mk_ngrams_patch.start()
        self.patches.append(mk_ngrams_patch)

        mongo_patch = patch('services.api.services.search.get_mongo_adapter')
        self.mocks['mongo_mock'] = mongo_patch.start()
        self.patches.append(mongo_patch)

        parser_patch = patch('services.api.services.search.SearchParser')
        self.mocks['parser_mock'] = parser_patch.start()
        self.patches.append(parser_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_init_creates_parser(self):
        # Setup
        mock_self = MagicMock()

        # Act
        SearchService.__init__(mock_self)

        # Assert
        self.mocks['parser_mock'].assert_called()

    def test_search_calls_methods_returns_result(self):
        # Setup
        mock_self = MagicMock(parser=MagicMock(field='search_term'))

        # Act
        SearchService.search(mock_self)

        # Assert
        mock_self._check_forbidden_characters.assert_called_with('search_term')
        mock_self._search_in_mongo.assert_called_with(
            self.mocks['mk_ngrams_mock'].return_value
        )

    def test_check_forbidden_characters_matches_calls_abort(self):
        # Setup
        mock_input = 'service_test'
        self.mocks['regex_mock'].match.return_value = True

        # Act
        SearchService._check_forbidden_characters(mock_input)

        # Assert
        self.mocks['abort_mock'].assert_called_with(
            403, extra='Invalid service name.'
        )

    def test_search_in_mongo_returns_mongo_call(self):
        # Setup
        request_ngrams = 'use user ser'

        # Act
        SearchService._search_in_mongo(request_ngrams)

        # Assert
        self.mocks['mongo_mock'].return_value.get_service_by_name\
            .assert_called_with('use user ser')

    def test_search_in_mongo_key_error_calls_abort(self):
        # Setup
        request_ngrams = 'use user ser'
        self.mocks['mongo_mock'].return_value.get_service_by_name\
            .side_effect = KeyError('Service not found.')

        # Act
        SearchService._search_in_mongo(request_ngrams)

        # Assert
        self.mocks['abort_mock'].assert_called_with(
            404, extra="'Service not found.'"
        )
