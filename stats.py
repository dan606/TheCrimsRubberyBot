from selenium.webdriver.common.by import By
from logger import *

from dataclasses import dataclass


@dataclass
class Stats:
    Intelligence: int
    Strength: int
    Charisma: int
    Tolerance: int

class stats():

    def __init__(self, browser):
        self.browser = browser
                  
    def get_toxic(self):
        try:
            current_toxic = self.browser.find_element(By.XPATH,'//div[@class="m+0rywACk0dJh3Za1YRM2w=="]').value_of_css_property("width")
            current_toxic = round(100*float(current_toxic[:-2])/128)
            return current_toxic
        except:
            logger.error("FAILED TO GET TOXIC")
            return -1

    def get_stamina(self):
        try:
            current_stamina = self.browser.find_element(By.XPATH,'//div[@class="AI8gJpfqwFNYI7UQIdIKXg=="]').value_of_css_property("width")
            current_stamina = round(100*float(current_stamina[:-2])/128)
            logger.info("LOADED STAMINA: " + str(current_stamina))
            return current_stamina
        except:
            logger.error("FAILED TO GET STAMINA")
            return -1

    def get_tickets(self):
        try:
            tickets = self.browser.find_element(By.XPATH,'//*[@id="username-char-respect"]/div[2]/div[2]/div').text
            current_tickets = int(tickets)
            logger.info("LOADED " + str(current_tickets) + " TICKETS")
            return current_tickets
        except:
            logger.error('FAILED TO LOAD TICKETS')
            return -1

    def get_stats(self):

        stats = Stats(-1,-1,-1,-1)

        try:
            allDiv2Elements = self.browser.find_elements(By.XPATH, "/html/body/div[2]/div[4]/div/table/tbody/tr/td[1]/div[2]/table/tbody/tr/td/div[3]/div/div[6]/div[2]/span")
            strength = -1
            tolerance = -1
            for e in allDiv2Elements:
                if len(e.text):
                    if strength == -1:
                        strength = int(e.text)
                    elif tolerance == -1:
                        tolerance = int(e.text)

            allDiv1Elements = self.browser.find_elements(By.XPATH, "/html/body/div[2]/div[4]/div/table/tbody/tr/td[1]/div[2]/table/tbody/tr/td/div[3]/div/div[6]/div[1]/span")
            intelligence = -1
            charisma = -1
            for e in allDiv1Elements:
                if len(e.text):
                    if intelligence == -1:
                        intelligence = int(e.text)
                    elif charisma == -1:
                        charisma = int(e.text)
            stats.Intelligence = intelligence
            stats.Strength = strength
            stats.Charisma = charisma
            stats.Tolerance = tolerance
            return stats
        except:
            return stats