from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from voting.models import Voting, Question, QuestionOption
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
    
    #Tests de la tarea M2F03   
    def test_ChartLoadPositive(self):
        
        votings = Voting.objects.all()
        
        if len(votings) > 0:
        
            self.driver.get('http://localhost:8000/visualizer/{}/'.format(votings[0].id))
            elements = self.driver.find_elements(By.ID, "piechart-censados")
            assert len(elements) > 0
            elements = self.driver.find_elements(By.ID, "piechart-genero")
            assert len(elements) > 0
            elements = self.driver.find_elements(By.ID, "barchart-poredad")
            assert len(elements) > 0
            assert self.driver.find_element(By.XPATH, "//span[contains(.,\'200\')]").text == "200"
        
    #Fin test de la tarea M2F03