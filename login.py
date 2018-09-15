#--coding:utf-8--
from selenium import webdriver
import time
import json


#browser=Chrome()

class Loginpage:
    def __init__(self,driver,url,username,password,verify_code):
        self.browser=driver
        self.browser.get(url)
        #登陆页面的各种输入框和按钮
        time.sleep(5)
        self.username_input=self.browser.find_element_by_id("acc-login")
        self.password_input=self.browser.find_element_by_id("pwd-login")
        self.login_button=self.browser.find_element_by_id("login-sure")
        self.phone_verify_input=self.browser.find_element_by_id("verify-code")
        self.login_verify_button=self.browser.find_element_by_id("commit")
        #用户输入的数据
        self.username=username
        self.phone_verify_code=verify_code

        self.password=password
    def logined(self):
        self.username_input.send_keys(self.username)
        self.password_input.send_keys(self.password)

        self.login_button.click()
        self.browser.maximize_window()
        #self.phone_verify_input.send_keys(self.phone_verify_code)
        #self.login_verify_button.click()

        #登录后获取cook
        #self.get_cook()

    def get_cook(self):
        time.sleep(2)
        cook=self.browser.get_cookies()
        return cook


