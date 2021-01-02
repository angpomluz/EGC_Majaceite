from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from voting.models import Voting

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
        
        votings = Voting.objects.all()
        
        if len(votings) > 0:
        
            self.driver.get('http://localhost:8000/visualizer/{}/'.votings[0])
            #In case of an existing voting, a element with id 'app-visualizer' is shown
            self.assertTrue(len(self.driver.find_elements_by_id('container-piechart-total')) > 0)

    def test_simpleIncorrectVisualizer(self):
        
        self.driver.get('http://localhost:8000/visualizer/999/')
        #In case of an inexisting voting, a element with id 'piechart-total' is shown
        elements = self.driver.find_elements(By.ID, "piechart-total")
        assert len(elements) == 0