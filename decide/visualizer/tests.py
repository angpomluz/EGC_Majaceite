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
from visualizer.utils import readCSV
from visualizer.utils import render_to_pdf
from visualizer.views import calculate_age, get_votes_by_age

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

    def test_get_visualizer(self):
        voting=self.create_voting()
        start={'action': 'start'}
        self.client.post('/voting/{}/'.format(voting.pk), start, format='json')
        stop={'action': 'stop'}
        self.client.post('/voting/{}/'.format(voting.pk), stop, format='json')
        tally={'action': 'tally'}
        self.client.post('/voting/{}/'.format(voting.pk), tally, format='json')
        data={'voting_id':voting.pk}
        response=self.client.get('/visualizer/{}/'.format(voting.pk),data,format='json')
        self.assertEqual(response.status_code,200)

    def test_get_visualizer_with_unexisting_voting(self):
        data={'voting_id':999}
        response=self.client.get('/visualizer/{}/'.format(999),data,format='json')
        self.assertEqual(response.status_code,404)

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
    
    def test_readCSV_positive(self):
        
        fpath="visualizer/resources/EGCusers.csv"
        read_users = readCSV(fpath)
        
        self.assertTrue(len(read_users) == 200)
        
    def test_readCSV_bad_path_negative(self):
        
        fpath="visualizer/resources/fakefile.csv"
        ex_catch = False
        try:
            readCSV(fpath)
        
        except(FileNotFoundError, IOError):
            ex_catch = True
            
        self.assertTrue(ex_catch)

    def test_readCSV_wrong_delimiter(self):
        
        fpath="visualizer/resources/EGCusersbaddelimiter.csv"
        err_triggered = False
        try:
            read_users = readCSV(fpath)            
        except(IndexError):
            err_triggered=True
        
        self.assertTrue(err_triggered)
            
    def test_get_votes_by_age_positive(self):
        
        read_users = readCSV("visualizer/resources/EGCusers.csv")
        
        age_range = [18,25,35,55,65]
        birthdates = [user['birthdate'] for user in read_users]
        votes_by_age = get_votes_by_age(age_range,birthdates)
        
        self.assertTrue(votes_by_age[18] > 0)
        
    def test_calculate_age_positive(self):
        
        born = "15/11/2000"
        age = calculate_age(born,True)
        
        self.assertTrue(age == 20)
        
    def test_calculate_age_bad_format_negative(self):
        
        err_triggered = False
        try:
            born = "2000/15/11"
            calculate_age(born,True)
            
        except(ValueError):
            err_triggered=True
        
        self.assertTrue(err_triggered)

    
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

    
    
class VisualizerTestCase3(BaseTestCase):
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

    def test_renderPDF_positive(self):
        fpath="visualizer/invoice.html"

        voting=self.create_voting()

        listed_values=[]
        Values=[0, 1, 'Unreal']
        listed_values.append(Values)
        context = {
        "voting_id": voting.pk,
        "voting_name": voting.name,
        "voting_question": voting.question,
        "data": listed_values,
        }
        render_template_response = render_to_pdf(fpath, context)
        
        self.assertTrue(len(render_template_response.items())>0)
    
    def test_renderPDF_positive_2(self):
        fpath="visualizer/invoice.html"

        voting=self.create_voting()

        listed_values=[]
        for d in voting.postproc:
            Values=[]
            for v in d.values():
                Values.append(v)
            listed_values.append(Values)
        context = {
        "voting_id": voting.pk,
        "voting_name": voting.name,
        "voting_question": voting.question,
        "data": listed_values,
        }
        render_template_response = render_to_pdf(fpath, context)
        print(render_template_response.items())
        self.assertTrue(len(render_template_response.items())>0)
