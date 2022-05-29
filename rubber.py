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
import signal

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

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
        self.counter = None
        self.current_tickets = -1
        self.current_stamina = -1
        self.current_toxic = -1
        self.signed_in = False

        while True:
            self.login()
            if self.current_tickets == -1:
                self.get_tickets()
            while self.current_tickets:
                self.robbery()
            self.logout()
            print("SLEEP FOR 1 HOUR, NO TICKETS")
            #time.sleep(67)

    def login(self, delay = 2):
        time.sleep(delay)
        self.log_in()
        time.sleep(delay)
        while self.get_tickets() == False:
            time.sleep(delay)
            self.log_in()
            time.sleep(delay)
        self.signed_in = True
        print("LOGIN SUCCESS")

    def logout(self):
        try:
            #logoutButton = self.browser.find_element(By.XPATH,"//*[@title='Logout')]")
            self.browser.get('https://www.thecrims.com/logout')
            self.signed_in = False
            print("LOGOUT SUCCESS")
            return True
        except:
            print("LOGOUT FAILED")
            return False
                  
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

    def checkToxic(self):
        if self.current_toxic == -1:
            print("GET TOXICITY")
            self.get_toxic()
        percent_toxic = round(100*float(self.current_toxic[:-2])/128)
        if percent_toxic > 9:
            print("TOXIC > 9, DO DETOX")
            self.detox()

    def robbery(self):
        print("AVAILABLE TICKETS: " + str(self.current_tickets))
        try:
            robberyButton = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-sprite-robbery"]')))
            if robberyButton:
                robberyButton.click()
                time.sleep(2)

                try:
                    useAllStamina = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Use all stamina')]/input")))
                    if useAllStamina:
                        if(useAllStamina.is_selected() == False):
                            useAllStamina.click()
                except ElementClickInterceptedException or StaleElementReferenceException or TimeoutException:
                    print("FAILED TO CLICK USE ALL STAMINA")            

                try:
                    robberySelection = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='singlerobbery-select-robbery']")))
                    select = Select(robberySelection)
                except ElementClickInterceptedException or StaleElementReferenceException or TimeoutException:
                    print("FAILED TO SELECT ROBBERY")
                    self.robbery()
        
                if select: #/// all options available under dropdown
                    last = None
                    for option in select.options: #// gets last iterator
                        #print(option.text, option.get_attribute('value')) 
                        if "100%" in option.text:
                            last = option.text
                    print("SELECTED ROBBERY: " + last)
                    self.get_stamina()
                    self.percent_stamina = round(100*float(self.current_stamina[:-2])/128)
                    print("STAMINA: " + str(self.percent_stamina) + "%")
                    select.select_by_visible_text(last) #//// picks the last element with 100% of chance to rob
                    if self.percent_stamina > 19:
                        print("RUBBER")
                        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//tr//table//tr//button[@id='singlerobbery-rob']"))).click()
                    else:
                        print("RESTORE STAMINA")
                        self.restore_stamina()
                        self.checkToxic()
                        self.robbery()
                    self.current_toxic = -1
        except ElementClickInterceptedException or StaleElementReferenceException or TimeoutException:
            print("IN EXCEPTION 2")
            self.robbery()

    def detox(self):
            hospital = WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menu-sprite-hospital"]')))
            if hospital:
                try:
                    hospital.click()
                    time.sleep(1)
                    detoxButton = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Detoxicate for cash']")))
                    if detoxButton:
                        detoxButton.click()
                        time.sleep(1)
                        self.current_toxic == -1
                        return True

                except ElementClickInterceptedException or StaleElementReferenceException:
                    return False
                    
                        
    def restore_stamina(self):
        random_club = random.randint(1,7)
        try:
            nightlife = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-sprite-nightlife"]')))
            if nightlife: 
                nightlife.click()
                time.sleep(1)
                try:
                    clubs = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, f'//ul[@class="bHz2Cti3p9UxZy4K1UQTQA== unstyled"]//li[{str(random_club)}]//*[@class="btn btn-inverse btn btn-inverse btn-small pull-right"]')))
                    if clubs:
                        clubs.click()
                        buyButton = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Buy']")))
                        if buyButton:
                            buyButton.click()
                            self.current_stamina = -1
                            self.current_tickets -= 1
                            exitButton = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[starts-with(@id, 'exit-button-')]")))
                            if exitButton:
                                exitButton.click()
                                time.sleep(1)
                            else:
                                print("FAILED TO EXIT CLUB")
                        else:
                            self.current_stamina = -1
                            print("FAILED TO BUY")
                except ElementClickInterceptedException or StaleElementReferenceException or TimeoutException:
                    print("FAILED TO SELECT CLUB")
                    self.current_stamina = -1
                    time.sleep(1)
                    self.restore_stamina()
        except ElementClickInterceptedException or StaleElementReferenceException or TimeoutException:
            print("FAILED TO SELECT NIGHTLIFE")
            self.current_stamina = -1
            time.sleep(1)
            self.restore_stamina()

inputParametersText = 'py <py file name> -l <login> -p <password>'

def main(argv):
    signal.signal(signal.SIGINT, signal_handler)

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