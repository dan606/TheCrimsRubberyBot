    def training(self):
        print("IN TRAINING STAMINA: " + str(self.current_stamina))
        if self.get_stamina():
            print("IN GET STAMINA")
            if self.current_stamina < 50:
                print("IN RESTORE")
                self.restore_stamina()
        else:
            print("FAILED TO GET STAMINA")
        try:
            trainigCenterButton = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-sprite-training"]')))
            if trainigCenterButton:
                trainigCenterButton.click()
                time.sleep(random.uniform(0.5, 2.9))

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

                print("STR: " + str(strength) + " INT: " + str(intelligence))
                time.sleep(random.uniform(0.8, 3.8))

                BuyButton = 0
                if strength < intelligence:
                    # gym button
                    BuyButton = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[4]/div/table/tbody/tr/td[1]/div[2]/table/tbody/tr/td/div[2]/div/div[3]/table[1]/tbody/tr[2]/td[3]/button")))
                else:
                    # education button
                    BuyButton = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[4]/div/table/tbody/tr/td[1]/div[2]/table/tbody/tr/td/div[2]/div/div[3]/table[2]/tbody/tr[2]/td[3]/button")))
                if BuyButton:
                    BuyButton.click()
                    time.sleep(random.uniform(1.0, 3.8))

                    try:
                        abortButton = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Abort']")))
                        if abortButton:
                            return True
                        else:
                            print("FAILED TO START TRAINING")
                            return False
                    except:
                        print("FAILED TO START TRAINING")
                        return False

                else:
                    return False
                    print("FAILED TO GET GYM OR EDUCATION BUTTON")
                
            else:
                print("FAILED TO GET TRAINING CENTER")
                return False
        except:
            print("TRAINING FAILED")
            return False
        return False