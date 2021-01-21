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
     
    def test_readvoitingwithouttally(self):
        self.driver.get(f'{self.live_server_url}/visualizer/6/')
        elements = self.driver.find_elements(By.XPATH, "//div[@id=\'app-visualizer\']/div/div/table/tbody/tr/td")
        assert len(elements) == 0    
    
    def test_visualizernonexistentvoting(self):
        self.driver.get(f'{self.live_server_url}/visualizer/77/')
        elements = self.driver.find_elements(By.ID, "piechart-total")
        assert len(elements) == 0


    def test_visualizebadvoting(self):
        self.driver.get(f'{self.live_server_url}/admin/login/?next=/admin/')
        self.driver.find_element(By.CSS_SELECTOR, "html").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("juanp")
        self.driver.find_element(By.ID, "id_password").send_keys("contrasena")
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
        self.driver.get(f'{self.live_server_url}/admin/voting/voting/355/change/')
        print(self.driver.current_url)
        #In case of a incorrect loging, a element errornote will be shown
        self.assertTrue(len(self.driver.find_elements_by_class_name('app-voting model-voting change-form vsc-initialized'))==0)

#Tests de la tarea M3F0D
class M3F0DTestCasesSelenium(StaticLiveServerTestCase):

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
    
    def test_chartDefensaLoadPositive(self):
        votings = Voting.objects.all()
        if len(votings) > 0:
            self.driver.get('http://localhost:8000/visualizer/{}/'.format(votings[0].id))
            elements = self.driver.find_elements(By.ID, "piechart-workstatus")
            assert len(elements) > 0