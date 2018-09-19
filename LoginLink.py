#--coding:utf-8--
from login import Loginpage


class LoginLinkParameters:

    def set_values(self,url,username,password,verify_code):
        self.username=username
        self.password=password
        self.verify_code=verify_code
        self.url=url


class LoginLink:
    def __init__(self,loginLinkParemeters):
        self.username=loginLinkParemeters.username
        self.password=loginLinkParemeters.password
        self.verify_code=loginLinkParemeters.verify_code
        self.url=loginLinkParemeters.url

    def execute_page(self,driver):
        loginpage=Loginpage(driver,self.url,self.username,self.password,self.verify_code)
        loginpage.logined()
        
        self.jar = loginpage.handle_cook()

    def get_cook(self):
        pass
    
        #取消弹窗
        #loginpage.cancel_prompt()



        
        

if __name__=="__main__":
    print('u 是个2b')