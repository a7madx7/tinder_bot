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
# Config and defaults region, alter upon your desires and at your own risk.
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
@dataclass
class Config:
    # Number Configs
    swipe_wait: float = 0.5
    short_wait: int = 1
    long_wait: int = 4
    soft_swipe_limit: int = 2000

    # Buttons XPathes
    login_btn_xpath: str = '//*[@id="u_0_0"]'
    popup1_btn_xpath: str = '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]'
    popup2_btn_xpath: str = '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]'

    popup3_btn_xpath: str = '//*[@id="modal-manager"]/div/div/div[2]/button[2]'
    match_popup_xpath: str = '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a'
    
    more_options_btn_xpath: str = '//*[@id="modal-manager"]/div/div/div/div/div[3]/span/button'
    like_btn_xpath: str = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button'
    dislike_btn_xpath: str = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button'
    accept_cookies_btn_xpath: str = '//*[@id="content"]/div/div[2]/div/div/div[1]/button'
    fb_btn_xpath: str = '//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button'
    
    # Inputs
    email_input_xpath: str = '//*[@id="email"]'
    pw_input_xpath: str = '//*[@id="pass"]'

    # URLs
    tinder_url: str = 'https://tinder.com'
    

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Bot class region.
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.config = Config()

    def accept_cookies(self):
        try:
            accept_cookies_btn = self.driver.find_element_by_xpath(self.config.accept_cookies_btn_xpath)
            accept_cookies_btn.click()
            return self
        except:
            return self

    def login(self):
        self.driver.get(self.config.tinder_url)

        sleep(self.config.long_wait)

        self.accept_cookies()

        # pressing more options button
        pressing_more_options = True
        while(pressing_more_options):
            try:
                more_options_btn = self.driver.find_element_by_xpath(self.config.more_options_btn_xpath)
                more_options_btn.click()
                pressing_more_options = False
            except Exception as e:
                print(e)
                print("Trying to press more options one more time...")
                sleep(self.config.short_wait)
                continue

        # pressing fb login button
        logging_in = True
        while(logging_in):
            try:
                fb_btn = self.driver.find_element_by_xpath(self.config.fb_btn_xpath)
                fb_btn.click()
                logging_in = False
            except Exception as e:
                print(e)
                print("Trying to press fb login one more time...")
                sleep(self.config.short_wait)
                continue

        # switch to login popup
        switching_to_login = True
        while(switching_to_login):
            try:
                base_window = self.driver.window_handles[0]
                self.driver.switch_to.window(self.driver.window_handles[1])
                switching_to_login = False
            except IndexError:
                print("Trying to switch windows one more time...")
                sleep(self.config.short_wait)
                continue

        email_in = self.driver.find_element_by_xpath(self.config.email_input_xpath)
        email_in.send_keys(username)

        pw_in = self.driver.find_element_by_xpath(self.config.pw_input_xpath)
        pw_in.send_keys(password)

        login_btn = self.driver.find_element_by_xpath(self.config.login_btn_xpath)
        login_btn.click()

        self.driver.switch_to.window(base_window)
        sleep(self.config.short_wait)
        closing_popup_1 = True
        while(closing_popup_1):
            try:
                popup_1 = self.driver.find_element_by_xpath(self.config.popup1_btn_xpath)
                popup_1.click()
                closing_popup_1 = False
            except:
                sleep(self.config.short_wait)
                print('Trying to close Popup 1...')
                continue

        closing_popup_2 = True
        while(closing_popup_2):
            try:
                popup_2 = self.driver.find_element_by_xpath(self.config.popup2_btn_xpath)
                popup_2.click()
                closing_popup_2 = False
            except:
                break

        return self

    def like(self):
        like_btn = self.driver.find_element_by_xpath(self.config.like_btn_xpath)
        like_btn.click()

    def dislike(self):
        dislike_btn = self.driver.find_element_by_xpath(self.config.dislike_btn_xpath)
        dislike_btn.click()

    def _swipe_right(self):
        sleep(self.config.swipe_wait)
        try:
            self.like()
            return True
        except:
            try:
                self.close_popup()
                return False
            except:
                try:
                    self.close_match()
                    return False
                except:
                    return False

    def auto_swipe(self):
        print('Initiating auto-swipe, it will take around 20 minutes to get the job done.')
        counter = 0
        while counter < self.config.soft_swipe_limit:
            if self._swipe_right():
                counter += 1
        print(f'Done auto-swiping {self.config.soft_swipe_limit} babes!!')

    def close_popup(self):
        popup_3 = self.driver.find_element_by_xpath(self.config.popup3_btn_xpath)
        popup_3.click()

    def close_match(self):
        match_popup = self.driver.find_element_by_xpath(self.config.match_popup_xpath)
        match_popup.click()

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Automation start region.
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

bot = TinderBot()
bot.login()

bot.auto_swipe()

