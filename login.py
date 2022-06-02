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
            log = self.browser.find_element(By.XPATH,'//input[@name="username"]')
            pas = self.browser.find_element(By.XPATH,'//input[@name="password"]')

            if log:
                try:
                    log.clear()
                    log.send_keys(f'{self.login_name}')
                except:
                    logger.error("problem with login name")
                    return False
            if pas:
                try:
                    pas.clear()
                    pas.send_keys(f'{self.login_password}')
                except:
                    logger.error("problem with password")
                    return False
            #if log.get_attribute("value") == f'{self.login_name}' and pas.get_attribute("value") == f'{self.login_password}':
            try:
                time.sleep(delay)
                #click_but = self.browser.find_element(By.XPATH,'//button[@class="btn btn-large btn-inverse btn-block"]')
                click_but = self.browser.find_element(By.XPATH,'//button[@type="submit"]')
                if click_but:
                    click_but.click()
                else:
                    print("LAMA")
                return self.checkIsSignedin()
            except:
                logger.error('problem with loging in')
                return False
        except:
            logger.error("problem to find login or password input")
            return False

    def logout(self):
        try:
            self.browser.get('https://www.thecrims.com/logout')
            self.is_signedin = False
            print("LOGOUT SUCCESS")
            return True
        except:
            print("LOGOUT FAILED")
            return False

    def checkIsSignedin(self):
        try:
            logoutButton = WebDriverWait(self.browser, random.uniform(1.3, 3.9)).until(EC.presence_of_element_located((By.XPATH,'//div[@class="m+0rywACk0dJh3Za1YRM2w=="]')))
            if logoutButton:
                self.is_signedin = True
                return True
            else:
                self.is_signedin = False
                return False
        except:
            self.is_signedin = False
            return False

