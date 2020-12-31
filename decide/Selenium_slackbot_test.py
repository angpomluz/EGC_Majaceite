#  
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
        
  def test_testbot(self):
    self.driver.get("https://app.slack.com/client/T01FX6E47EG/C01FJ9JHHNJ")
    self.driver.set_window_size(1536, 824)
    self.driver.find_element(By.CSS_SELECTOR, ".p-channel_sidebar__channel--selected > .p-channel_sidebar__name").click()
    self.driver.find_element(By.CSS_SELECTOR, ".ql-editor > p").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".ql-editor")
    self.driver.execute_script("if(arguments[0].contentEditable === 'true') {arguments[0].innerText = '<p>-res_v3</p>'}", element)
    self.driver.find_element(By.CSS_SELECTOR, ".c-icon--paperplane-filled").click()
    self.driver.execute_script("window.scrollTo(0,0)")
    assert self.driver.find_element(By.CSS_SELECTOR, ".c-message_kit__hover--hovered .c-message_kit__text").text == "Estos son los resultados de la votacion 3:\\\\n-->Opcion 0: (Claro que si) -- Votos obtenidos: (2)\\\\n-->Opcion 1: (Claro que no) -- Votos obtenidos: (1)"
  
