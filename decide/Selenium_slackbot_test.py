#  
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from base.tests import BaseTestCase

class AdminTestCase(StaticLiveServerTestCase):

  """
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
        
  def test_seleniumslacktest(self):
    self.driver.get("https://resultadosegc.slack.com/")
    self.driver.set_window_size(945, 1020)
    self.driver.find_element(By.ID, "email").send_keys("PruebasEGC99@gmail.com")
    self.driver.find_element(By.ID, "password").send_keys("paraprobar99")
    self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)
    self.driver.execute_script("window.scrollTo(0,0)")
    self.driver.find_element(By.CSS_SELECTOR, ".p-channel_sidebar__channel--selected > .p-channel_sidebar__name").click()
    element1 = self.driver.find_element(By.CSS_SELECTOR, "#\\31 609422055\\.003700 .c-base_icon")
    actions1 = ActionChains(self.driver)
    actions1.move_to_element(element1).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".ql-editor > p").send_keys("-res_v3")
    self.driver.find_element(By.CSS_SELECTOR, ".c-icon--paperplane-filled").click()
    self.driver.execute_script("window.scrollTo(0,0)")
    assert self.driver.find_element(By.CSS_SELECTOR, ".c-message_kit__hover--hovered .c-message_kit__text").text == "Estos son los resultados de la votacion 3:\\\\n-->Opcion 0: (Claro que si) -- Votos obtenidos: (2)\\\\n-->Opcion 1: (Claro que no) -- Votos obtenidos: (1)"
  
  def test_seleniumslacknegativetest(self):
    self.driver.get("https://app.slack.com/workspace-signin?redir=%2Fgantry%2Fauth%3Fapp%3Dclient%26lc%3D1609421501%26return_to%3D%252Fclient%252FT01FX6E47EG%252FC01FJ9JHHNJ%26teams%3D")
    self.driver.set_window_size(945, 1020)
    self.driver.find_element(By.ID, "domain").send_keys("ResultadosEGC")
    self.driver.find_element(By.CSS_SELECTOR, ".c-button").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".c-button")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.ID, "email").click()
    self.driver.find_element(By.ID, "email").send_keys("PruebasEGC99@gmail.com")
    self.driver.find_element(By.ID, "password").send_keys("paraprobar99")
    self.driver.find_element(By.ID, "signin_btn").click()
    self.driver.find_element(By.CSS_SELECTOR, ".ql-editor > p").click()
    self.driver.find_element(By.CSS_SELECTOR, ".ql-editor > p").send_keys("-estonosesuncomando")
    text = self.driver.find_element(By.CSS_SELECTOR, ".c-message_list > .c-scrollbar__hider").text
    assert text != "Nuevo"
  """