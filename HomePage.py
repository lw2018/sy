import time

from selenium import webdriver


class HomePage:
    def __init__(self,driver,one_left_menus):
        #self.home_menu = driver.find_element_by_link_text("工作台")
        self.send_menu = driver.find_element_by_link_text("发送首营")
        self.menu = one_left_menus
        self.driver=driver

    def ask_menu(self):
        pass
    def click_ask_menu(self):
        self.ask_menu
        pass

    def click_send_menu(self):
        time.sleep(2)
        self.send_menu.click()

    def cancel_prompt(self): 
        #提示信息框
        promt = self.driver.find_elements_by_id("layui-layer1")
        if promt != []:   #提示框里面的x按钮
            self.driver.find_element_by_xpath("//*[@id='layui-layer1']/span[1]/a").click()
            print("提示")
        time.sleep(3)
