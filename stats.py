class stats():

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