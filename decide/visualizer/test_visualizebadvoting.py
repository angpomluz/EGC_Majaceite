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
    
    def test_visualizebadvoting(self):
        self.driver.get("http://localhost:8010/admin/login/?next=/admin/")
        self.driver.find_element(By.CSS_SELECTOR, "html").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("juanp")
        self.driver.find_element(By.ID, "id_password").send_keys("contrasena")
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
        self.driver.find_element(By.LINK_TEXT, "Votings").click()
        self.driver.find_element(By.CSS_SELECTOR, ".warning").click()
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".warning")
        assert len(elements) > 0
  