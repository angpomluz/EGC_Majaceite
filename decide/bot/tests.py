from django.test import TestCase
from django_telegrambot.apps import DjangoTelegramBot
from bot.telegrambot import getVoting

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from base.tests import BaseTestCase

import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from voting.models import Voting, Question, QuestionOption
from django.utils import timezone
from mixnet.models import Auth
from django.conf import settings

class TelegramTestBot(StaticLiveServerTestCase):
    
    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        self.base.tearDown()
    
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

# Tests bot
    
    # ESTOS TEST SOLO SE PUEDEN RUNEAR EL LOCAL DEBIDO A LA DEPENDENCIA DE NGROK
    # Y FALLARIAN AL HACER LA BUILD EN TRAVIS
    
    # def test_getvoting(self):
    #     votingId = self.create_voting().id
    #     self.assertIsNotNone(getVoting(votingId))
    
    # def test_botsettings(self):
    #     mode = settings.DJANGO_TELEGRAMBOT['MODE']
    #     assert mode == 'WEBHOOK'
    #     site = settings.DJANGO_TELEGRAMBOT['WEBHOOK_SITE']
    #     assert site == settings.BASEURL + '/admin/django-telegrambot'
    #     prefix = settings.DJANGO_TELEGRAMBOT['WEBHOOK_PREFIX']
    #     assert prefix == '/prefix'
    
    # def test_tokenbot(self):
    #     bot = DjangoTelegramBot
    #     bot_tokens = bot.bot_tokens
    #     bot_token = bot_tokens[0]
    #     self.assertEquals(bot_token, '1478165863:AAGTc2kVAoGTI1-pZck4ZvkNYho2ldB_NX8')
        
    # def test_loginisneccessary(self):
    #     self.driver.get(f'{settings.BASEURL}/bot/')
    #     self.driver.find_element(By.LINK_TEXT, "Django-Telegrambot Dashboard").click()
    #     elements = self.driver.find_elements(By.ID, "id_username")
    #     assert len(elements) > 0
    
    # def test_assertview(self):
    #     self.driver.get(f'{settings.BASEURL}/bot/')
    #     self.driver.find_element(By.LINK_TEXT, "Django-Telegrambot Dashboard").click()
    #     self.driver.find_element(By.ID, "id_username").send_keys("administrador")
    #     self.driver.find_element(By.ID, "id_password").send_keys("admin1234")
    #     self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
    #     title = self.driver.find_elements(By.LINK_TEXT, "Django-TelegramBot")
    #     assert len(title) > 0
    #     bot_mode = self.driver.find_element(By.XPATH, "//h3[contains(.,\'Bot update mode: WEBHOOK\')]").text
    #     assert bot_mode == "Bot update mode: WEBHOOK"
    #     bot_list = self.driver.find_element(By.XPATH, "//h3[contains(.,\'Bot List:\')]").text
    #     assert bot_list == "Bot List:"
    
    # def test_assertbotexists(self):
    #     self.driver.get(f'{settings.BASEURL}/bot/')
    #     self.driver.find_element(By.LINK_TEXT, "Django-Telegrambot Dashboard").click()
    #     self.driver.find_element(By.ID, "id_username").send_keys("administrador")
    #     self.driver.find_element(By.ID, "id_password").send_keys("admin1234")
    #     self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
    #     elements = self.driver.find_elements(By.LINK_TEXT, "@EGCTestBot")
    #     assert len(elements) > 0