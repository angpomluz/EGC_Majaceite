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
        
    def test_simpleCorrectLogin(self):                    
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("qwerty",Keys.ENTER)
        
        print(self.driver.current_url)
        #In case of a correct loging, a element with id 'user-tools' is shown in the upper right part
        self.assertTrue(len(self.driver.find_elements_by_id('user-tools'))==1)
        
    def test_simpleWrongLogin(self):                    
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element_by_id('id_username').send_keys("baduser")
        self.driver.find_element_by_id('id_password').send_keys("badpass",Keys.ENTER)
        
        print(self.driver.current_url)
        #In case of a incorrect loging, a element errornote will be shown
        self.assertTrue(len(self.driver.find_elements_by_class_name('errornote'))==1)
        
    def test_CreateQuestion(self):
        self.driver.get(f'{self.live_server_url}/admin/login/?next=/admin/')
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("administrador")
        self.driver.find_element(By.ID, "id_password").send_keys("administrador")
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
        self.driver.find_element(By.LINK_TEXT, "Questions").click()
        self.driver.find_element(By.CSS_SELECTOR, ".addlink").click()
        self.driver.find_element(By.ID, "id_desc").send_keys("test question")
        self.driver.find_element(By.ID, "id_options-0-option").click()
        self.driver.find_element(By.ID, "id_options-0-option").send_keys("test option")
        self.driver.find_element(By.ID, "id_options-0-number").click()
        self.driver.find_element(By.ID, "id_options-0-number").send_keys("1")
        self.driver.find_element(By.NAME, "_save").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".row1:nth-child(1) a").text == "test question"
        
    def test_ejercicio5(self):
        self.driver.get(f'{self.live_server_url}/admin/login/?next=/admin/')
        self.driver.find_element(By.ID, "id_username").send_keys("administrador")
        self.driver.find_element(By.ID, "id_password").send_keys("administrador")
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
    
    
        
    

        
        
    