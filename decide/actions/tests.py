from django.test import TestCase
from django.conf import settings
from base.tests import BaseTestCase
import slack

class ActionModelTest(BaseTestCase):

    def test_response_Bot_notfromslack(self):
        data = {} 
        self.login()
        response = self.client.post('/actions/event/hook', data, format= 'json')
        self.assertEquals(response.status_code, 301)
