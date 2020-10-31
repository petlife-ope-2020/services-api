import unittest
from unittest.mock import patch

from services.api.routes.search import Search


# pylint: disable=protected-access
class SearchTestCase(unittest.TestCase):

    def setUp(self):
        self.patches = []
        self.mocks = {}

        flask_resource_patch = patch('services.api.routes.search.Resource')
        self.mocks['flask_resource_mock'] = flask_resource_patch.start()
        self.patches.append(flask_resource_patch)

        creation_service_patch = patch('services.api.routes.search.SearchService')
        self.mocks['search_service_mock'] = creation_service_patch.start()
        self.patches.append(creation_service_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_post_returns_creation_service_call(self):
        # Act
        Search.get()

        # Assert
        self.mocks['search_service_mock'].return_value.search.assert_called()
