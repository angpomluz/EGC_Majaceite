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
        postprocs=[]
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
            postOpt={'votes':0,'number':i,'option':'option {}'.format(i+1),'postproc':0}
            postprocs.append(postOpt)
        v = Voting(name='test voting', question=q)
        v.postproc=postprocs
        v.start_date=timezone.now()
        v.end_date=timezone.now()
        v.tally=5
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v
    #Voting without starting date
    def create_voting1(self):
        q = Question(desc='test question')
        q.save()
        postprocs=[]
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
            postOpt={'votes':0,'number':i,'option':'option {}'.format(i+1),'postproc':0}
            postprocs.append(postOpt)
        v = Voting(name='voting without starting date', question=q)
        v.postproc=postprocs
        v.tally=5
        v.save()
        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v
    #Voting without ending date
    def create_voting2(self):
        q = Question(desc='test question')
        q.save()
        postprocs=[]
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
            postOpt={'votes':0,'number':i,'option':'option {}'.format(i+1),'postproc':0}
            postprocs.append(postOpt)
        v = Voting(name='voting without ending date', question=q)
        v.postproc=postprocs
        v.start_date=timezone.now()
        v.tally=5
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v
    #Voting without tally
    def create_voting3(self):
        q = Question(desc='test question')
        q.save()
        postprocs=[]
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
            postOpt={'votes':0,'number':i,'option':'option {}'.format(i+1),'postproc':0}
            postprocs.append(postOpt)
        v = Voting(name='test voting', question=q)
        v.postproc=postprocs
        v.start_date=timezone.now()
        v.end_date=timezone.now()
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    def test_download_results_in_csv_format(self):
        # We must create a voting
        voting=self.create_voting()
        start={'action': 'start'}
        self.client.post('/voting/{}/'.format(voting.pk), start, format='json')
        stop={'action': 'stop'}
        self.client.post('/voting/{}/'.format(voting.pk), stop, format='json')
        tally={'action': 'tally'}
        self.client.post('/voting/{}/'.format(voting.pk), tally, format='json')
        #Download in csv format
        data={'VotID':voting.pk,'Formato':'csv'}
        response=self.client.get('/downloadResults/',data,format='json')
        self.assertEqual(response.status_code,200)

    def test_download_results_in_json_format(self):
        # We must create a voting
        voting=self.create_voting()
        start={'action': 'start'}
        self.client.post('/voting/{}/'.format(voting.pk), start, format='json')
        stop={'action': 'stop'}
        self.client.post('/voting/{}/'.format(voting.pk), stop, format='json')
        tally={'action': 'tally'}
        self.client.post('/voting/{}/'.format(voting.pk), tally, format='json')
        #Download in json format
        data={'VotID':voting.pk,'Formato':'json'}
        response=self.client.get('/downloadResults/',data,format='json')
        self.assertEqual(response.status_code,200)

    def test_download_results_in_xml_format(self):
        # We must create a voting
        voting=self.create_voting()
        start={'action': 'start'}
        self.client.post('/voting/{}/'.format(voting.pk), start, format='json')
        stop={'action': 'stop'}
        self.client.post('/voting/{}/'.format(voting.pk), stop, format='json')
        tally={'action': 'tally'}
        self.client.post('/voting/{}/'.format(voting.pk), tally, format='json')
        data={'VotID':voting.pk,'Formato':'xml'}
        response=self.client.get('/downloadResults/',data,format='json')
        self.assertEqual(response.status_code,200)

    def test_trying_to_download_results_when_voting_not_started(self):
        voting=self.create_voting1()
        data={'VotID':voting.pk,'Formato':'csv'}
        response=self.client.get('/downloadResults/',data,format='json')
        self.assertEqual(response.status_code,404)
    
    def test_trying_to_download_results_when_voting_not_ended(self):
        voting=self.create_voting2()
        start={'action': 'start'}
        self.client.post('/voting/{}/'.format(voting.pk), start, format='json')
        data={'VotID':voting.pk,'Formato':'csv'}
        response=self.client.get('/downloadResults/',data,format='json')
        self.assertEqual(response.status_code,404)
    
    def test_trying_to_download_results_when_voting_not_tallied(self):
        voting=self.create_voting3()
        start={'action': 'start'}
        self.client.post('/voting/{}/'.format(voting.pk), start, format='json')
        stop={'action': 'stop'}
        self.client.post('/voting/{}/'.format(voting.pk), stop, format='json')
        data={'VotID':voting.pk,'Formato':'csv'}
        response=self.client.get('/downloadResults/',data,format='json')
        self.assertEqual(response.status_code,404)

    
class VisualizerTestCase2(BaseTestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def create_voting(self):
        q = Question(desc='test question')
        q.save()
        postprocs=[]
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
            postOpt={'votes':0,'number':i,'option':'option {}'.format(i+1),'postproc':0}
            postprocs.append(postOpt)
        v = Voting(name='test voting', question=q)
        v.postproc=postprocs
        v.start_date=timezone.now()
        v.end_date=timezone.now()
        v.tally=5
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    def test_download_results_in_pdf_format(self):
        # We must create a voting
        voting=self.create_voting()
        start={'action': 'start'}
        self.client.post('/voting/{}/'.format(voting.pk), start, format='json')
        stop={'action': 'stop'}
        self.client.post('/voting/{}/'.format(voting.pk), stop, format='json')
        tally={'action': 'tally'}
        self.client.post('/voting/{}/'.format(voting.pk), tally, format='json')
        #Download in pdf format
        data={'VotID':voting.pk,'Formato':'pdf'}
        response=self.client.get('/downloadResults/',data,format='json')
        self.assertEqual(response.status_code,200)
    

        



