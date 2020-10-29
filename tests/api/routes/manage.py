import unittest
from unittest.mock import patch

from services.api.routes.manage import Manage


# pylint: disable=protected-access
class ManageTestCase(unittest.TestCase):

    def setUp(self):
        self.patches = []
        self.mocks = {}

        flask_resource_patch = patch('services.api.routes.manage.Resource')
        self.mocks['flask_resource_mock'] = flask_resource_patch.start()
        self.patches.append(flask_resource_patch)

        creation_service_patch = patch('services.api.routes.manage.CreationService')
        self.mocks['creation_service_mock'] = creation_service_patch.start()
        self.patches.append(creation_service_patch)

        addition_service_patch = patch('services.api.routes.manage.AdditionService')
        self.mocks['addition_service_mock'] = addition_service_patch.start()
        self.patches.append(addition_service_patch)

    def tearDown(self):
        for patch_ in self.patches:
            patch_.stop()

    def test_post_returns_creation_service_call(self):
        # Act
        Manage.post()

        # Assert
        self.mocks['creation_service_mock'].return_value.create.assert_called()

    def test_put_returns_addition_service_call(self):
        # Act
        Manage.put()

        # Assert
        self.mocks['addition_service_mock'].return_value.add.assert_called()
