#--coding:utf-8--
from HomePage import HomePage
import time 
#登陆进来后的主页

class HomePageLinkParameters:
    def set_values(self,one_left_menus=1):
        self.menu = one_left_menus

class HomePageLink:
    def __init__(self,homePageLinkParemeters):
        self.menu = homePageLinkParemeters.menu

    def execute_page(self,driver):
        time.sleep(1)
        homePage = HomePage(driver,self.menu)
        homePage.cancel_prompt()

        time.sleep(3)
        homePage.click_send_menu()
