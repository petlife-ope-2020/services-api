import unittest
from unittest.mock import MagicMock, patch, call

from services.api.body_parsers.removal import RemovalParser


# pylint: disable=protected-access
class RemovalParserTestCase(unittest.TestCase):

    def setUp(self):
        self.patches = []
        self.mocks = {}

        flask_parser_patch = patch('services.api.body_parsers.removal.RequestParser')
        self.mocks['flask_parser_mock'] = flask_parser_patch.start()
        self.patches.append(flask_parser_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_init_creates_parser_parse_args(self):
        # Setup
        mock_self = MagicMock()
        parser_calls = [
            call(
                name='petshop_username',
                type=str,
                location='args',
                required=True
            ),
            call(
                name='service_id',
                type=str,
                location='args',
                required=True
            )
        ]

        # Act
        RemovalParser.__init__(mock_self)

        # Assert
        self.mocks['flask_parser_mock'].return_value.\
            add_argument.assert_has_calls(parser_calls)
