import random
import itertools
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from base import mods
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from voting.tests import VotingTestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from base.tests import BaseTestCase
from voting.models import Voting, Question, QuestionOption

# Create your tests here.

class VisualizerTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def create_voting(self):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    def test_download_results(self):
        # We must create a voting
        voting=create_voting()
        start={'action': 'start'}
        self.client.post('/voting/{}/'.format(voting.pk), start, format='json')
        stop={'action': 'stop'}
        self.client.post('/voting/{}/'.format(voting.pk), stop, format='json')
        tally={'action': 'tally'}
        self.client.post('/voting/{}/'.format(voting.pk), tally, format='json')
        response=self.client.get('/downloadResults/',{'VotID':voting.pk},format='json')
        self.assertEqual(response.status_code,200)
        


