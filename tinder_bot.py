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
from selenium.common.exceptions import NoSuchElementException
import random

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
    short_wait: float = 1
    long_wait: float = 2
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

class AI():
    def praise_the_bitch(self):
        praises = ['Awe that girl was hot dude', 'I guess ur gonna get what u see my man', 
        "Nigga this bitch ain't for hookups", "That curvy babe <3", "Will you marry me?",
        "That's a hell of an ass my dude!", "Saw dat bitch? daaaaamn", "Fuck my life", "How cute!"]
        print(random.choice(praises))
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Bot class region.
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.config = Config()
        self.ai = AI()

    def _accept_cookies(self):
        try:
            self._click_a_button(self.config.accept_cookies_btn_xpath)
            return self
        except:
            return self

    def _fill_credentials(self):
        self.driver.find_element_by_xpath(self.config.email_input_xpath).send_keys(username)
        self.driver.find_element_by_xpath(self.config.pw_input_xpath).send_keys(password)
        self._click_a_button(self.config.login_btn_xpath)
        print("Done filling credentials")

    def _like(self):
        self._click_a_button(self.config.like_btn_xpath)
        
    def _dislike(self):
        self._click_a_button(self.config.dislike_btn_xpath)
    def _swipe_right(self):
        sleep(self.config.swipe_wait)
        try:
            self._like()
            self.ai.praise_the_bitch()
            return True
        except:
            try:
                self._click_a_button(self.config.popup3_btn_xpath)
                return False
            except:
                try:
                    self._close_match()
                    return False
                except:
                    return False

    def _click_a_button(self, xpath):
        self.driver.find_element_by_xpath(xpath).click()

    def _close_all_popups(self):
        try:
            self._click_a_button(self.config.popup1_btn_xpath)
        except:
            try:
                self._click_a_button(self.config.popup2_btn_xpath)
            except:
                try:
                    self._click_a_button(self.config.popup3_btn_xpath)
                except:
                    raise Exception("It's about time you review your bot for tinder changes!")
                
    def _close_match(self):
        self._click_a_button(self.config.match_popup_xpath)

    def _persist_pressing_a_button(self, xpath):
        pressing = True
        while(pressing):
            try:
                self._click_a_button(xpath)
                pressing = False
            except NoSuchElementException as ex:
                sleep(self.config.short_wait)
                continue

    def _switch_to_login(self):
        # switch to login window
        switching_to_login = True
        while(switching_to_login):
            try:
                base_window = self.driver.window_handles[0]
                self.driver.switch_to.window(self.driver.window_handles[1])
                switching_to_login = False
                self._fill_credentials()
                self.driver.switch_to.window(base_window)
                return True
            except IndexError:
                print("Trying to switch windows one more time...")
                sleep(self.config.short_wait)
                continue

    def _element_exists(self, xpath):
        """
        Used mainly to check for Tinder antibot procedures.
        """
        try:
            self.driver.find_element_by_xpath(xpath)
            return True
        except NoSuchElementException as e:
            print("Tinder is trying to prevent us, that won't help it a lot though...")
            return False

    def _attempt_login(self):
        if self._element_exists(self.config.fb_btn_xpath):
            self._persist_pressing_a_button(self.config.fb_btn_xpath)
        elif self._element_exists(self.config.login_btn_xpath):
            self._persist_pressing_a_button(self.config.login_btn_xpath)
            sleep(self.config.swipe_wait)
            self._persist_pressing_a_button(self.config.fb_btn_xpath)
            self._persist_pressing_a_button(self.config.more_options_btn_xpath)
        elif self._element_exists(self.config.more_options_btn_path):
            self._persist_pressing_a_button(self.config.more_options_btn_xpath)
            self._persist_pressing_a_button(self.config.fb_btn_xpath)
    def login(self):
        self.driver.get(self.config.tinder_url)
        print("TinderBot is starting, please wait...")
        sleep(self.config.long_wait)

        self._accept_cookies()
        self._attempt_login()

        self._switch_to_login()

        self._persist_pressing_a_button(self.config.popup1_btn_xpath)
        self._persist_pressing_a_button(self.config.popup2_btn_xpath)
        return self

    

    def auto_swipe(self):
        print('Initiating auto-swipe, it will take around 20 minutes to get the job done.')
        counter = 0
        while counter < self.config.soft_swipe_limit:
            if self._swipe_right():
                counter += 1
        print(f'Done auto-swiping {self.config.soft_swipe_limit} babes!!')
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Automation start region.
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

bot = TinderBot()
bot.login()

bot.auto_swipe()

