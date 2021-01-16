from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from voting.models import Voting, Question, QuestionOption
from base.tests import BaseTestCase


class M2F04TestCasesSelenium(StaticLiveServerTestCase):

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
    
    def test_seleniumslack(self):
        self.driver.get("https://resultadosegc.slack.com/")
        self.driver.set_window_size(1920, 1040)
        self.driver.find_element(By.ID, "email").send_keys("PruebasEGC99@gmail.com")
        self.driver.find_element(By.ID, "password").send_keys("paraprobar99")
        self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)
        self.driver.get("https://app.slack.com/client/T01FX6E47EG/D01JHGDARFG")
        assert self.driver.find_element(By.CSS_SELECTOR, ".p-classic_nav_member_name").text == "EGC"