# frozen_string_literal: true

require 'selenium-webdriver'
require_relative 'secrets.rb'

class Config
  attr_accessor :swipe_wait, :short_wait, :long_wait, :soft_swipe_limit,
                :login_btn_xpath, :popup1_btn_xpath, :popup2_btn_xpath, :popup3_btn_xpath,
                :match_popup_xpath, :more_options_btn_xpath, :like_btn_xpath, :dislike_btn_xpath,
                :accept_cookies_btn_xpath, :fb_btn_xpath, :email_input_xpath, :pw_input_xpath, :tinder_url,
                :fb_username, :fb_password
  def initialize
    @swipe_wait = 0.5
    @short_wait = 1
    @long_wait =  2
    @soft_swipe_limit = 2000
    @login_btn_xpath = '//*[@id="u_0_0"]'
    @popup1_btn_xpath = '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]'
    @popup2_btn_xpath = '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]'
    @popup3_btn_xpath = '//*[@id="modal-manager"]/div/div/div[2]/button[2]'
    @match_popup_xpath = '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a'
    @more_options_btn_xpath = '//*[@id="modal-manager"]/div/div/div/div/div[3]/span/button'
    @like_btn_xpath = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button'
    @dislike_btn_xpath = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button'
    @accept_cookies_btn_xpath = '//*[@id="content"]/div/div[2]/div/div/div[1]/button'
    @fb_btn_xpath = '//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button'
    @email_input_xpath = '//*[@id="email"]'
    @pw_input_xpath = '//*[@id="pass"]'
    @tinder_url = 'https://tinder.com'
    @fb_username = Secrets::Credentials[:username]
    @fb_password = Secrets::Credentials[:password]
  end
end

class AI
  def praise_the_bitch
    puts ['Awe that girl was hot dude', 'I guess ur gonna get what u see my man',
          "Nigga this bitch ain't for hookups", 'That curvy babe <3', 'Will you marry me?',
          "That's a hell of an ass my dude!", 'Saw dat bitch? daaaaamn', 'Fuck my life', 'How cute!'].sample
  end
end
class TinderBot
  def initialize
    @driver = Selenium::WebDriver.for :chrome
    @config = Config.new
    @ai = AI.new
  end

  def login
    @driver.navigate.to @config.tinder_url
    puts "TinderBot is starting, please wait..."
    sleep @config.long_wait

    accept_cookies
    attempt_login

    switch_to_login

    persist_pressing_a_button @config.popup1_btn_xpath
    persist_pressing_a_button @config.popup2_btn_xpath
    self
  end

  def auto_swipe
    puts 'Initiating auto-swipe, it will take around 20 minutes to get the job done.'
    counter = 0

    while counter < @config.soft_swipe_limit
      if swipe_right
        counter += 1
      end
    end
    puts "Done auto-swiping #{@config.soft_swipe_limit} babes!!"
  end

  private

  def element_exists?(xpath)
    # Used mainly to check for Tinder antibot procedures.
    @driver.find_element(xpath: xpath)
    return true
  rescue Selenium::WebDriver::Error::NoSuchElementError => e
    puts "Tinder is trying to prevent us, that won't help it a lot though..."
    return false
  end

  def attempt_login
    if element_exists?(@config.fb_btn_xpath)
      persist_pressing_a_button @config.fb_btn_xpath
    elsif element_exists?(@config.login_btn_xpath)
      persist_pressing_a_button @config.login_btn_xpath
      sleep @config.swipe_wait
      persist_pressing_a_button @config.fb_btn_xpath
      persist_pressing_a_button @config.more_options_btn_xpath
    elsif element_exists?(@config.more_options_btn_xpath)
      persist_pressing_a_button @config.more_options_btn_xpath
      persist_pressing_a_button @config.fb_btn_xpath
    end
  end

  def persist_pressing_a_button(xpath)
    pressing = true
    while pressing
      begin
        click_a_button xpath
        pressing = false
      rescue Selenium::WebDriver::Error::NoSuchElementError => e
        sleep @config.short_wait
        next
      end
    end
  end

  def switch_to_login
    switching = true
    while switching
      begin
        base_window = @driver.window_handles[0]
        @driver.switch_to.window(@driver.window_handles[1])
        switching = false
        fill_credentials
        @driver.switch_to.window(base_window)
        return true
      rescue StandardError
        puts 'Trying to switch windows one more time...'
        sleep(@config.short_wait)
        next
      end
    end
  end

  def fill_credentials
    begin
      @driver.find_element(xpath: @config.email_input_xpath)
             .send_keys(@config.fb_username)
      @driver.find_element(xpath: @config.pw_input_xpath)
             .send_keys(@config.fb_password)
      click_a_button @config.login_btn_xpath
    rescue StandardError
    end
    puts 'Done filling credentials'
    self
  end

  def accept_cookies
    click_a_button @config.accept_cookies_btn_xpath
    puts 'Accepted cookies successfully!'
    self
  rescue StandardError => e
    puts "Couldn't accept cookies cause #{e}"
  end

  def click_a_button xpath 
    @driver.find_element(xpath: xpath).click
  end

  def close_all_popups
    click_a_button @config.popup1_btn_xpath
    true
  rescue StandardError
    begin
      click_a_button @config.popup2_btn_xpath
      true
    rescue StandardError
      begin
        click_a_button @config.popup3_btn_xpath
        true
      rescue StandardError
        # If everything fails then we're stuck at the login page.
        restart_login_modal
      end
    end
  end

  def close_a_match
    click_a_button @config.match_popup_xpath
  end

  def like
    click_a_button @config.like_btn_xpath
  end

  def dislike
    click_a_button @config.dislike_btn_xpath
  end

  def swipe_right
    sleep @config.swipe_wait
    begin
      like
      @ai.praise_the_bitch
      true
    rescue StandardError
      begin
        click_a_button @config.popup3_btn_xpath
        false
      rescue StandardError => e
        begin
          close_a_match
          false
        rescue StandardError => e
          false
        end
      end
    end
  end
end

bot = TinderBot.new
bot.login.auto_swipe
