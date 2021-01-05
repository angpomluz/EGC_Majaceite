from django.test import TestCase
from django.conf import settings
from base.tests import BaseTestCase

class ActionModelTest(BaseTestCase):

    def test_response_Bot_notfromslack(self):
        data = {} #El campo action es requerido en la request
        self.login()
        response = self.client.get('/actions/event/hook', data, format= 'json')
        self.assertEquals(response.status_code, 301)
