# CopyRight: 2020 Dr. Ahmad Hamdi Emara 
"""
Requires chrome-webdriver to be installed and matched with the current version of chrome installation.
Requires selenium: install it via pip3 install selenium.
Requires Python 3.7 or later.
Please run with python3 tinder_bot.py not with python tinder_bot.py.
"""

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Imports region.
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
from selenium import webdriver

"""
Create a secrets file right next to tinder_bot and put two string variables
there containing Your facebook credentials.
"""
from secrets import username, password
from dataclasses import dataclass

from time import sleep

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Constants and defaults region, alter upon your desires and at your own risk.
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
@dataclass
class Constants:
    swipe_wait: float = 0.5
    short_wait: int = 1
    long_wait: int = 2
    login_btn_xpath: str = '//*[@id="u_0_0"]'
    popup1_btn_xpath: str = '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]'
    popup2_btn_xpath: str = '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]'


    ### 
    # Todo: certain bug, Tinder has changed the xpath for the next two elements
    # But I can't seem to get a working case to get their respective xpathes.
    ###
    popup3_btn_xpath: str = '//*[@id="modal-manager"]/div/div/div[2]/button[2]'
    match_popup_xpath: str = '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a'


    accept_cookies_btn_xpath: str = '//*[@id="content"]/div/div[2]/div/div/div[1]/button'
    fb_btn_xpath: str = '//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button'
    email_input_xpath: str = '//*[@id="email"]'
    pw_input_xpath: str = '//*[@id="pass"]'
    tinder_url: str = 'https://tinder.com'
    more_options_btn_xpath: str = '//*[@id="content"]/div/div[1]/div/div/main/div/div[2]/div[2]/div/div/span/button'
    like_btn_xpath: str = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button'
    dislike_btn_xpath: str = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button'

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Bot class region.
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.constants = Constants()

    def accept_cookies(self):
        try:
            accept_cookies_btn = self.driver.find_element_by_xpath(self.constants.accept_cookies_btn_xpath)
            accept_cookies_btn.click()
            return self
        except:
            return self

    def login(self):
        self.driver.get(self.constants.tinder_url)

        sleep(self.constants.long_wait)

        self.accept_cookies()

        try:
            more_options_btn = self.driver.find_element_by_xpath(self.constants.more_options_btn_xpath)
            more_options_btn.click()
        except:
            pass
        

        fb_btn = self.driver.find_element_by_xpath(self.constants.fb_btn_xpath)
        fb_btn.click()

        # switch to login popup
        switching_to_login = True
        while(switching_to_login):
            try:
                base_window = self.driver.window_handles[0]
                self.driver.switch_to.window(self.driver.window_handles[1])
                switching_to_login = False
            except IndexError:
                print("Trying to switch windows one more time.")
                sleep(self.constants.short_wait)
                continue

        email_in = self.driver.find_element_by_xpath(self.constants.email_input_xpath)
        email_in.send_keys(username)

        pw_in = self.driver.find_element_by_xpath(self.constants.pw_input_xpath)
        pw_in.send_keys(password)

        login_btn = self.driver.find_element_by_xpath(self.constants.login_btn_xpath)
        login_btn.click()

        self.driver.switch_to.window(base_window)
        sleep(self.constants.short_wait)
        closing_popup_1 = True
        while(closing_popup_1):
            try:
                popup_1 = self.driver.find_element_by_xpath(self.constants.popup1_btn_xpath)
                popup_1.click()
                closing_popup_1 = False
            except:
                sleep(self.constants.short_wait)
                print('Trying to close Popup 1')
                continue

        closing_popup_2 = True
        while(closing_popup_2):
            try:
                popup_2 = self.driver.find_element_by_xpath(self.constants.popup2_btn_xpath)
                popup_2.click()
                closing_popup_2 = False
            except:
                break

        return self

    def like(self):
        like_btn = self.driver.find_element_by_xpath(self.constants.like_btn_xpath)
        like_btn.click()

    def dislike(self):
        dislike_btn = self.driver.find_element_by_xpath(self.constants.dislike_btn_xpath)
        dislike_btn.click()

    def auto_swipe(self):
        print('Initiating auto-swipe !!')
        while True:
            sleep(self.constants.swipe_wait)
            try:
                self.like()
            except Exception:
                try:
                    self.close_popup()
                except Exception:
                    try:
                        self.close_match()
                    except Exception:
                        continue

    def close_popup(self):
        popup_3 = self.driver.find_element_by_xpath(self.constants.popup3_btn_xpath)
        popup_3.click()

    def close_match(self):
        match_popup = self.driver.find_element_by_xpath(self.constants.match_popup_xpath)
        match_popup.click()

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Automation start region.
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

bot = TinderBot()
# from ruby best practices: you can method chain the next two lines like this bot.login().auto_swipe()
# as they return self, just left it unchained for simplicity.
bot.login()
bot.auto_swipe()
