import unittest
from unittest.mock import MagicMock, patch

from services.api.body_parsers.search import SearchParser


# pylint: disable=protected-access
class SearchParserTestCase(unittest.TestCase):

    def setUp(self):
        self.patches = []
        self.mocks = {}

        flask_parser_patch = patch('services.api.body_parsers.search.RequestParser')
        self.mocks['flask_parser_mock'] = flask_parser_patch.start()
        self.patches.append(flask_parser_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_init_creates_parser_parse_args(self):
        # Setup
        mock_self = MagicMock()

        # Act
        SearchParser.__init__(mock_self)

        # Assert
        self.mocks['flask_parser_mock'].return_value.\
            add_argument.assert_called_with(
                name='service_name',
                type=str,
                location='args',
                required=True
            )
