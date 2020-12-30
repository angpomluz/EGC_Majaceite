import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","decide.settings")
import django
django.setup()

from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from base.tests import BaseTestCase

class AdminTestCase(StaticLiveServerTestCase):


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
    
    def test_simpleCorrectVisualizer(self):
        
        self.driver.get('http://localhost:8000/visualizer/1/')
        #In case of an existing voting, a element with id 'app-visualizer' is shown
        self.assertTrue(len(self.driver.find_elements_by_id('app-visualizer')) > 1)

    def test_simpleIncorrectVisualizer(self):
        
        self.driver.get('http://localhost:8000/visualizer/999/')
        #In case of an inexisting voting, a element with id 'summary' is shown
        self.assertTrue(len(self.driver.find_elements_by_id('summary')) > 1)