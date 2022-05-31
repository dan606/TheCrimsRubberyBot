from logger import *

class login():
    self.is_signedin = False

    def __init__(self, loginName, loginPassword, browser):

        logger.info("Login INIT")
        self.browser = browser
        self.login_name = loginName
        self.login_password = loginPassword

    def login(self, delay = 2):
        time.sleep(delay)
        self.log_in()
        time.sleep(delay)
        while self.get_tickets() == False:
            time.sleep(delay)
            self.log_in()
            time.sleep(delay)
        self.is_signedin = True
        print("LOGIN SUCCESS")

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

    def log_in(self):
        #log = self.browser.find_element(By.XPATH,'//input[@placeholder="Username"]')
        try:
            log = self.browser.find_element(By.XPATH,'//*[@id="loginform"]/input[1]')
            pas = self.browser.find_element(By.XPATH,'//input[@name="password"]')
        except:
            print("problem to find login or password input")
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
                time.sleep(random.uniform(0.5, 2.5))
                click_but = self.browser.find_element(By.XPATH,'//button[@class="btn btn-large btn-inverse btn-block"]') 
                click_but.click()
            except:
                print('problem with loging in')