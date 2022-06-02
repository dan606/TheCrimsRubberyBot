from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import random
from datetime import datetime

class crims_robber():
    
    def __init__(self, browser):
        self.browser = browser

        self.current_tickets = -1
        self.current_stamina = -1
        self.current_toxic = -1
                  
    def get_toxic(self):
        try:
            self.current_toxic = self.browser.find_element(By.XPATH,'//div[@class="m+0rywACk0dJh3Za1YRM2w=="]').value_of_css_property("width")
            self.current_toxic = round(100*float(self.current_toxic[:-2])/128)
            return True
        except:
            print("FAILED TO GET TOXIC")
            self.current_toxic = -1
            return False

    def get_stamina(self):
        try:
            self.current_stamina = self.browser.find_element(By.XPATH,'//div[@class="AI8gJpfqwFNYI7UQIdIKXg=="]').value_of_css_property("width")
            self.current_stamina = round(100*float(self.current_stamina[:-2])/128)
            print("LOADED STAMINA: " + str(self.current_stamina))
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

    def checkToxic(self):
        if self.current_toxic == -1:
            print("GET TOXICITY")
            self.get_toxic()
        if self.current_toxic > 9:
            print("TOXIC > 9, DO DETOX")
            self.detox()

    def robbery(self):
        try:
            robberyButton = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-sprite-robbery"]')))
            if robberyButton:
                robberyButton.click()
                time.sleep(random.uniform(0.5, 3.8))
                try:
                    useAllStamina = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Use all stamina')]/input")))
                    if useAllStamina:
                        if(useAllStamina.is_selected() == False):
                            useAllStamina.click()
                except:
                    print("FAILED TO CLICK USE ALL STAMINA")            

                try:
                    robberySelection = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='singlerobbery-select-robbery']")))
                    select = Select(robberySelection)
                except:
                    print("FAILED TO SELECT ROBBERY")
                    return False
        
                if select: #/// all options available under dropdown
                    last = None
                    for option in select.options: #// gets last iterator
                        #print(option.text, option.get_attribute('value')) 
                        if "100%" in option.text:
                            last = option.text
                    print("SELECTED ROBBERY: " + last)

                    divider_position = int(last.rfind(" - ", 0))
                    percentage_position = int(last.rfind("% ", 0))
                    needed_stamina = -1
                    if divider_position and percentage_position:
                        needed_stamina = int(last[divider_position+3:percentage_position])
                    self.get_stamina()
                    print("STAMINA: " + str(self.current_stamina) + "%")
                    select.select_by_visible_text(last) #//// picks the last element with 100% of chance to rob
                    if self.current_stamina >= needed_stamina:
                        print("RUBBER")
                        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//tr//table//tr//button[@id='singlerobbery-rob']"))).click()
                    else:
                        print("RESTORE STAMINA")
                        self.restore_stamina()
                        self.checkToxic()
                    self.current_toxic = -1
        except:
            print("ROBBERY FAILED")
            return False

    def detox(self):
            hospital = WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menu-sprite-hospital"]')))
            if hospital:
                try:
                    hospital.click()
                    time.sleep(random.uniform(0.5, 1.9))
                    detoxButton = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Detoxicate for cash']")))
                    if detoxButton:
                        detoxButton.click()
                        time.sleep(random.uniform(0.9, 2.9))
                        self.current_toxic == -1
                        return True

                except:
                    return False
                    
                        
    def restore_stamina(self):

        if self.current_stamina == -1:
            self.get_stamina()
        
        if self.current_stamina > 50:
            return False

        random_club = random.randint(1,7)
        try:
            nightlife = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-sprite-nightlife"]')))
            if nightlife: 
                nightlife.click()
                time.sleep(random.uniform(0.5, 3.8))
                try:
                    clubs = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, f'//ul[@class="bHz2Cti3p9UxZy4K1UQTQA== unstyled"]//li[{str(random_club)}]//*[@class="btn btn-inverse btn btn-inverse btn-small pull-right"]')))
                    if clubs:
                        clubs.click()
                        random.uniform(0.3, 1.9)
                        buyButton = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Buy']")))
                        if buyButton:
                            buyButton.click()
                            random.uniform(0.3, 1.9)
                            self.current_stamina = -1
                            self.current_tickets -= 1
                            exitButton = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[starts-with(@id, 'exit-button-')]")))
                            if exitButton:
                                exitButton.click()
                                time.sleep(random.uniform(0.5, 3.8))
                                return True
                            else:
                                print("FAILED TO EXIT CLUB")
                                return False
                        else:
                            self.current_stamina = -1
                            print("FAILED TO BUY")
                            return False
                except:
                    print("FAILED TO SELECT CLUB")
                    self.current_stamina = -1
                    return False
        except:
            print("FAILED TO SELECT NIGHTLIFE")
            self.current_stamina = -1
            return False