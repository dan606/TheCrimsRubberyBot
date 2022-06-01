from logger import *
from login import *
from rubber import *
from tasks import *

import sys, getopt, signal, psutil
from selenium.webdriver import ActionChains
import undetected_chromedriver.v2 as uc
import random

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

inputParametersText = 'py <py file name> -l <login> -p <password>'

def main(argv):
    signal.signal(signal.SIGINT, signal_handler)

    loginName = ''
    password = ''
    try:
        opts, args = getopt.getopt(argv,"hl:p:",["login=","password="])
    except:
        print(inputParametersText)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            logger.warn(inputParametersText)
            sys.exit()
        elif opt in ("-l", "--login"):
            loginName = arg
        elif opt in ("-p", "--password"):
            password = arg
    if not loginName or not password:
        logger.error("NO LOGIN OR PASSWORD")
        logger.fatal(inputParametersText)
        sys.exit(2)
    logger.info('login: ' + loginName)
    logger.info('password len: ' + str(len(password)))

    while True:
        try:
            browser = uc.Chrome()
            #self.browser = webdriver.Chrome()
            browser.get("https://www.thecrims.com/")
            action = ActionChains(browser)

#            time.sleep(2)
            Login = login(loginName, password, browser)
            Robber = crims_robber(browser)
            Stats = stats(browser)

            logger.info("BOT inicialized")

            while True:
                Login.login(random.uniform(0.5, 3.8))
                while Login.is_signedin == False:
                    time.uniform(1, 2.9)
                    Login.login(random.uniform(0.5, 3.8))
                
                if Stats.current_tickets == -1:
                    Stats.get_tickets()
                while Stats.current_tickets > 1:
                    Robber.robbery()
                for i in range(2):
                    if Robber.training():
                        break
                Login.logout()
                minutesSleep = random.randint(30, 60)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print(current_time + " SLEEP FOR " + str(minutesSleep) + " MIN, NO TICKETS")
                time.sleep((60 * minutesSleep) + random.randint(0, 59))


        except:
            try:
                for p in psutil.process_iter():
                    if "chrome" in p.name():
                        p.kill()
                Robber = crims_robber(browser)
            except:
                logger.fatal("FAILED TO START BOT")
                break

if __name__ == "__main__":
   main(sys.argv[1:])