import unittest
from unittest.mock import MagicMock, patch, call

from services.api.body_parsers.addition import AdditionParser


# pylint: disable=protected-access
class AdditionParserTestCase(unittest.TestCase):

    def setUp(self):
        self.patches = []
        self.mocks = {}

        flask_parser_patch = patch('services.api.body_parsers.addition.RequestParser')
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
                name='service_id',
                type=str,
                location='json',
                required=True
            ),
            call(
                name='petshop_username',
                type=str,
                location='json',
                required=True
            ),
            call(
                name='petshop_name',
                type=str,
                location='json',
                required=True
            )
        ]

        # Act
        AdditionParser.__init__(mock_self)

        # Assert
        self.mocks['flask_parser_mock'].return_value.\
            add_argument.assert_has_calls(parser_calls)
