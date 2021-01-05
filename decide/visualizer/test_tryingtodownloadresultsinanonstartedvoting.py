import pytest
import time
import json
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from voting.models import Voting
from base.tests import BaseTestCase
"""
class TestTryingtodownloadresultsinanonstartedvoting():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_tryingtodownloadresultsinanonstartedvoting(self):
      #Change the Id of Visualizer to a known Id 
    self.driver.get("http://localhost:8000/visualizer/2/")
    self.driver.set_window_size(797, 824)
    assert self.driver.find_element(By.CSS_SELECTOR, "h2").text == "Votación no comenzada"
"""

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

