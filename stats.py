from selenium.webdriver.common.by import By

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
            print("FAILED TO GET TOXIC")
            return -1

    def get_stamina(self):
        try:
            current_stamina = self.browser.find_element(By.XPATH,'//div[@class="AI8gJpfqwFNYI7UQIdIKXg=="]').value_of_css_property("width")
            current_stamina = round(100*float(current_stamina[:-2])/128)
            print("LOADED STAMINA: " + str(current_stamina))
            return current_stamina
        except:
            print("FAILED TO GET STAMINA")
            return -1

    def get_tickets(self):
        try:
            tickets = self.browser.find_element(By.XPATH,"//*[contains(text(), 'Tickets:')]").text
            current_tickets = int(tickets[9:])
            print("LOADED " + str(current_tickets) + " TICKETS")
            return current_tickets
        except:
            tickets = self.browser.find_element(By.XPATH,"/html/body/div[2]/div[4]/div/table/tbody/tr/td[1]/div[2]/table/tbody/tr/td/div[3]/div/div[1]/div[1]/div[12]/span").text
            if tickets:
                current_tickets = int(tickets)
                print("LOADED METHOD 2 " + str(current_tickets) + " TICKETS")
                return current_tickets
            else:
                print("FAILED TO GET TICKETS")
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