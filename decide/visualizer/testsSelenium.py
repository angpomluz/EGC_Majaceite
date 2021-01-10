from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from voting.models import Voting, Question, QuestionOption
from base.tests import BaseTestCase


class M2F03TestCasesSelenium(StaticLiveServerTestCase):

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
        
class TestDownloadResults(StaticLiveServerTestCase):
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
        
    def test_downloadvotingresultsindifferentformats(self):
        votings = Voting.objects.all()
        if len(votings) > 0:
            self.driver.get('http://localhost:8000/visualizer/{}/'.votings[0])
            self.driver.set_window_size(797, 824)
            elements = self.driver.find_elements(By.CSS_SELECTOR, "input:nth-child(3)")
            assert len(elements) > 0
            self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(3)").click()
            self.driver.find_element(By.NAME, "Formato").click()
            dropdown = self.driver.find_element(By.NAME, "Formato")
            dropdown.find_element(By.XPATH, "//option[. = 'CSV']").click()
            self.driver.find_element(By.NAME, "Formato").click()
            self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(3)").click()
            self.driver.find_element(By.NAME, "Formato").click()
            dropdown = self.driver.find_element(By.NAME, "Formato")
            dropdown.find_element(By.XPATH, "//option[. = 'XML']").click()
            self.driver.find_element(By.NAME, "Formato").click()
            self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(3)").click()
            self.driver.find_element(By.NAME, "Formato").click()
            dropdown = self.driver.find_element(By.NAME, "Formato")
            dropdown.find_element(By.XPATH, "//option[. = 'PDF']").click()
            self.driver.find_element(By.NAME, "Formato").click()
            self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(3)").click()
            
class TestTryingToDownloadResultsNotStartedVoting(StaticLiveServerTestCase):
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
        
    def test_tryingtodownloadresultsinanonstartedvoting(self):
        votings = Voting.objects.all()
        if len(votings) > 0:
            self.driver.get('http://localhost:8000/visualizer/{}/'.votings[0])
            self.driver.set_window_size(797, 824)
            assert self.driver.find_element(By.CSS_SELECTOR, "h2").text == "Votación no comenzada"
            
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
        """
        self.driver.get('http://localhost:8000/visualizer/999/')
        #In case of an inexisting voting, a element with id 'piechart-total' is shown
        elements = self.driver.find_elements(By.ID, "piechart-total")
        assert len(elements) == 0
        """

