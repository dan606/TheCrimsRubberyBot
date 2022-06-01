from logger import *

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import time
import random

class login():
    def __init__(self, loginName, loginPassword, browser):
        self.browser = browser
        self.login_name = loginName
        self.login_password = loginPassword
        self.is_signedin = False

    def login(self, delay = 2):
        #log = self.browser.find_element(By.XPATH,'//input[@placeholder="Username"]')
        try:
            log = self.browser.find_element(By.XPATH,'//*[@id="loginform"]/input[1]')
            pas = self.browser.find_element(By.XPATH,'//input[@name="password"]')
        except:
            logger.error("problem to find login or password input")
        logged = None
        if log:
            try:
                log.clear()
                log.send_keys(f'{self.login_name}')
            except:
                logger.error("problem with login")
        if pas:
            try:
                pas.clear()
                pas.send_keys(f'{self.login_password}')
            except:
                logger.error("problem with password")
        if log.get_attribute("value") == f'{self.login_name}' and pas.get_attribute("value") == f'{self.login_password}':
            try:
                time.sleep(random.uniform(0.5, 2.5))
                click_but = self.browser.find_element(By.XPATH,'//button[@class="btn btn-large btn-inverse btn-block"]')
                click_but.click()
                logger.info("SIGNED IN")
            except:
                logger.error('problem with loging in')

    def logout(self):
        try:
            #logoutButton = self.browser.find_element(By.XPATH,"//*[@title='Logout')]")
            self.browser.get('https://www.thecrims.com/logout')
            self.is_signedin = False
            print("LOGOUT SUCCESS")
            return True
        except:
            print("LOGOUT FAILED")
            return False

