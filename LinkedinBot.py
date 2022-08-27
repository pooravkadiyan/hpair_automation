"""LinkedinBot.py: By now, only helps in sending connection requests to HPAIR members."""

__author__      = "Poorav Kadiyan"
__copyright__   = "Copyright 2022, Poorav Kadiyan"

import argparse
import selenium
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException    
import time
import csv
import os
import ssl

"""
    This class is used to LinkedIn stuff focused for HPAIR automation.

"""
class LinkedinBot():
    #Initializations
    ssl._create_default_https_context = ssl._create_unverified_context
    
    #Constructor
    def __init__(self, username, password) -> None:

        self.username = username
        self.password = password
        

    """
        This method is used to login to linkedin.
    """
    def login(self, driver) -> None:
        driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")  
        uname_field = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]')))
        uname_field.send_keys(self.username)
        password_field = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))
        password_field.send_keys(self.password)
        login_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="organic-div"]/form/div[3]/button')))
        login_button.click()
        time.sleep(5)
      
    """
        This method is used to get the linkedin_id of HPAIR members.
    
    """


    def get_id_list(self,file_name='hpair_delegates.csv') -> list:
        file_path = os.path.join(os.path.dirname(__file__),file_name)
        with open(file_path, newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            id_links = []
            for row in data:
                id_link = row[4]
                if 'linkedin' in id_link:
                    if 'https:' not in id_link:
                        id_link = 'https:' + id_link
                    else:
                        id_link = id_link

                    id_links.append(id_link)
                else:
                    pass
            return id_links

    """
        This method is used to send connection requests to HPAIR members.
    """
    def connect(self,id_links,driver) -> None:
        for id_link in id_links:
            driver.get(id_link)

            try:
                xyz1_buttons = driver.find_elements(By.XPATH, '//*[@class="artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action"]')
                connect_button = xyz1_buttons[1]
                connect_button.click()
                time.sleep(3)

                send_button = driver.find_element(By.XPATH, "//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml1']")
                send_button.click()

            except NoSuchElementException:
                follow_button = driver.find_element(By.XPATH,'//*[@data-control-name="topcard_primary_follow" and @class="pvs-profile-actions__action artdeco-button artdeco-button--2 artdeco-button--primary ember-view"]')
                follow_button.click()

            except Exception as e:
                print(e)
                pass

                time.sleep(2)
                i+=1
                print('Done with ' + str(i) + ' requests')

        return None
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process the LinkedIn Bot Inputs') 
    parser.add_argument('--username', help='LinkedIn_UserId', required=True)
    parser.add_argument('--password', help='LinkedIn_Password', required=True)
    args = parser.parse_args()
    username = args.username
    password = args.password

    bot = LinkedinBot(username, password)
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    bot.login(driver)
    id_links = bot.get_id_list()
    print(id_links)
    bot.connect(id_links,driver)
    driver.quit()
    print('Done')
    
    








    
    





