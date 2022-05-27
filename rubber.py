from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as UI
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
import time
import psutil
import os
import shutil
import random
import undetected_chromedriver.v2 as uc

class crims_robber():
    
    def __init__(self, login, password, counter=0):
        self.login = login
        self.password = password

        try:
            self.browser = uc.Chrome()
            self.browser.get("https://www.thecrims.com/")
        except:
            print("DRIVER FAILED")

        # self.browser = webdriver.Chrome("D:\Projects\HACKS\TC-BOT\chromedriver.exe")
        # self.browser.get("https://www.thecrims.com/")
        self.action = ActionChains(self.browser)
        self.rob_power = 10
        self.number = 6
        self.counter = None

        self.current_toxic = -1

        self.log_in()
        while self.get_toxic() == False:
            time.sleep(3)
            self.log_in()
            time.sleep(0.5)
        while True:
            self.robbery()
            time.sleep(1)
#        while True:
#            self.restore_stamina()
                  
    def get_toxic(self):
        try:
            self.current_toxic = self.browser.find_element(By.XPATH,'//div[@class="m+0rywACk0dJh3Za1YRM2w=="]').value_of_css_property("width")
            return True
        except:
            print("FAILED TO GET TOXIC")
            self.current_toxic = -1
            return False

    def get_stamina(self):
        try:
            self.current_stamina = self.browser.find_element(By.XPATH,'//div[@class="AI8gJpfqwFNYI7UQIdIKXg=="]').value_of_css_property("width")
            return True
        except:
            print("FAILED TO GET STAMINA")
            self.current_stamina = -1
            return False

    def log_in(self):
        #log = self.browser.find_element(By.XPATH,'//input[@placeholder="Username"]')
        log = self.browser.find_element(By.XPATH,'//*[@id="loginform"]/input[1]')
        pas = self.browser.find_element(By.XPATH,'//input[@name="password"]')
        logged = None
        if log:
            try:
                log.clear()
                log.send_keys(f'{self.login}')
            except:
                print("problem with login")
        if pas:
            try:
                pas.clear()
                pas.send_keys(f'{self.password}')
            except:
                print("problem with password")
        if log.get_attribute("value") == f'{self.login}' and pas.get_attribute("value") == f'{self.password}':
            try:
                time.sleep(1)
                click_but = self.browser.find_element(By.XPATH,'//button[@class="btn btn-large btn-inverse btn-block"]') 
                click_but.click()
            except:
                print('problem with loging in')
    

    def robbery(self):
        if self.current_toxic == -1:
            print("UNLOADED TOXIC")
            return

        print("TOXIC: " + self.current_toxic)

        percent_toxic = round(100*float(self.current_toxic[:-2])/128)
        try:
            if percent_toxic > 9:
                self.toxic()
            else:
                print("IN ELSE")
                but = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-sprite-robbery"]')))
                if but:
                    print("IN BUT")
                    but.click()
                    time.sleep(2)
                    robberySelection = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='singlerobbery-select-robbery']")))
                    select = Select(robberySelection)
                
                    if select: #/// all options available under dropdown
                        last = None
                        for option in select.options: #// gets last iterator
                            print(option.text, option.get_attribute('value')) 
                            if "100%" in option.text:
                                last = option.text
                        print("LAST: " + last)
                        self.get_stamina()
                        self.percent_stamina = round(100*float(self.current_stamina[:-2])/128)
                        print("STAMINA: " + str(self.percent_stamina) + "%")
                        select.select_by_visible_text(last) #//// picks the last element with 100% of chance to rob
                        if self.percent_stamina > 49:
                            print("RUBBER")
                            WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//tr//table//tr//button[@id='singlerobbery-rob']"))).click()
                        else:
                            self.restore_stamina()
                            self.robbery()
        except ElementClickInterceptedException or StaleElementReferenceException or TimeoutException:
            print("IN EXCEPTION")
            self.robbery()

        #//// checks toxiacation and proceeds
    def toxic(self):
            hospital = WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menu-sprite-hospital"]')))
            if hospital:
                try:
                    hospital.click()
                    time.sleep(1)
                    detoxButton = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Detoxicate for cash']")))
                    if detoxButton:
                        detoxButton.click()
                        time.sleep(1)
                        self.robbery()

                except ElementClickInterceptedException or StaleElementReferenceException:
                    self.robbery()
                    
                        
    def restore_stamina(self):
        self.random_club = random.randint(1,5)
        try:
            nightlife = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-sprite-nightlife"]')))
            if nightlife: 
                nightlife.click()
                time.sleep(1)
                clubs = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, f'//ul[@class="bHz2Cti3p9UxZy4K1UQTQA== unstyled"]//li[{str(self.random_club)}]//*[@class="btn btn-inverse btn btn-inverse btn-small pull-right"]'))) #.click()
                if clubs:
                    clubs.click()
                    time.sleep(1)
                    buyButton = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Buy']")))
                    if buyButton:
                        buyButton.click()
                        self.current_stamina = -1
                        time.sleep(1)
                        exitButton = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[class='btn btn-inverse btn btn-inverse' & text()='Exit']")))
                        if exitButton:
                            print("IN EXIT BUTTON")
                            exitButton.click()
                            sleep(1)
                    else:
                        self.current_stamina = -1
                        print("ERRRROR")
        except ElementClickInterceptedException or StaleElementReferenceException or TimeoutException:
            self.current_stamina = -1
            time.sleep(1)
            self.restore_stamina()
                
    def restore(self):
        self.get_stamina()
        self.percent_stamina = round(100*float(self.current_stamina[:-2])/128)
        try:
            stamina_number = []
            inside_club = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.XPATH,"//table[@class='table table-condensed table-top-spacing']//tbody//tr//td[2]")))
            stamina_number.extend([float(elem.text[:-1]) for elem in inside_club]) #// saves each element text as float so it can be compared in next step
            try:
                for i in inside_club:
                    print("CLUB: " + i)
                    #if float(i.text[:-1]) == max(stamina_number):
                        #needed_to_100 = 100/max(stamina_number)
                        #needed_now = self.percent_stamina/max(stamina_number)
                        #final_score = (needed_to_100 - needed_now)
                        #i.find_element_by_xpath("./following::td/input[@name='quantity']").click()
                        #i.find_element_by_xpath("./following::td/input[@name='quantity']").send_keys(f'{round(final_score)}')
                        #i.find_element_by_xpath("./following::td/button[@class='btn btn-inverse btn-small']").click()
            
            except ElementClickInterceptedException or StaleElementReferenceException:
                self.robbery()
               
        except TimeoutException:
            self.restore_stamina()
        

if __name__ == "__main__":
    login = "assiniss" #// put your login here
    password = "dcba7ec5d38a" #// put your password here
    try:
        app = crims_robber(login, password)
    except:
        try:
            for p in psutil.process_iter():
                if "chrome" in p.name():
                    p.kill()
            app = crims_robber(login, password)
        except psutil.NoSuchProcess:
            app = crims_robber(login, password)