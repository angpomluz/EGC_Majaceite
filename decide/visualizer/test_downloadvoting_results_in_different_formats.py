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
class TestDownloadvotingresultsindifferentformats():
  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_downloadvotingresultsindifferentformats(self):
      #Change Id of visualizer to a known Id
    self.driver.get("http://localhost:8000/visualizer/1/")
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

"""
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
  

    

