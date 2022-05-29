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
import sys, getopt

class crims_robber():
    
    def __init__(self, loginName, loginPassword, counter=0):
        self.login_name = loginName
        self.login_password = loginPassword

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

        self.login()
        while True:
            if self.current_toxic == -1:
                self.get_toxic()
            self.robbery()
            time.sleep(2)

    def login(self, delay = 2):
        time.sleep(delay)
        self.log_in()
        time.sleep(delay)
        while self.get_tickets() == False:
            time.sleep(delay)
            self.log_in()
            time.sleep(delay)
        print("LOGIN SUCCESS")

    def logout(self):
        try:
            #logoutButton = self.browser.find_element(By.XPATH,"//*[@title='Logout')]")
            self.browser.get('https://www.thecrims.com/logout')
            print("LOGOUT SUCCESS")
            return True
        except:
            print("LOGOUT FAILED")
            return False
                  
    def get_toxic(self):
        try:
                                                                                 # m+0rywACk0dJh3Za1YRM2w==
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

    def get_tickets(self):
        try:
            tickets = self.browser.find_element(By.XPATH,"//*[contains(text(), 'Tickets:')]").text
            self.current_tickets = int(tickets[9:])
            print("LOADED " + str(self.current_tickets) + " TICKETS")
            return True
        except:
            print("FAILED TO GET TICKETS")
            self.current_tickets = -1
            return False

    def log_in(self):
        #log = self.browser.find_element(By.XPATH,'//input[@placeholder="Username"]')
        log = self.browser.find_element(By.XPATH,'//*[@id="loginform"]/input[1]')
        pas = self.browser.find_element(By.XPATH,'//input[@name="password"]')
        logged = None
        if log:
            try:
                log.clear()
                log.send_keys(f'{self.login_name}')
            except:
                print("problem with login")
        if pas:
            try:
                pas.clear()
                pas.send_keys(f'{self.login_password}')
            except:
                print("problem with password")
        if log.get_attribute("value") == f'{self.login_name}' and pas.get_attribute("value") == f'{self.login_password}':
            try:
                time.sleep(1)
                click_but = self.browser.find_element(By.XPATH,'//button[@class="btn btn-large btn-inverse btn-block"]') 
                click_but.click()
            except:
                print('problem with loging in')
    

    def robbery(self):
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
#                    try:
                    robberySelection = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='singlerobbery-select-robbery']")))
                    select = Select(robberySelection)
#                    except ElementClickInterceptedException or StaleElementReferenceException or TimeoutException:
#                        print("IN EXCEPTION 1")
#                        self.robbery()
            
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
                        if self.percent_stamina > 19:
                            print("RUBBER")
                            WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//tr//table//tr//button[@id='singlerobbery-rob']"))).click()
                        else:
                            self.restore_stamina()
                            self.robbery()
                        self.current_toxic = -1
        except ElementClickInterceptedException or StaleElementReferenceException or TimeoutException:
            print("IN EXCEPTION 2")
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
        self.random_club = random.randint(3,10)
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
                        time.sleep(0.5)
                        exitButton = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[starts-with(@id, 'exit-button-')]")))
                        if exitButton:
                            print("IN EXIT BUTTON")
                            exitButton.click()
                            time.sleep(1)
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


inputParametersText = 'py <py file name> -l <login> -p <password>'

def main(argv):
    login = ''
    password = ''
    try:
        opts, args = getopt.getopt(argv,"hl:p:",["login=","password="])
    except getopt.GetoptError:
        print(inputParametersText)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(inputParametersText)
            sys.exit()
        elif opt in ("-l", "--login"):
            login = arg
        elif opt in ("-p", "--password"):
            password = arg
    if not login or not password:
        print("NO LOGIN OR PASSWORD")
        print(inputParametersText)
        sys.exit(2)
    print ('login: ' + login)
    print ('password len: ' + str(len(password)))

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

if __name__ == "__main__":
   main(sys.argv[1:])