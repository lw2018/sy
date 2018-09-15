#--coding:utf-8--
from SendFirst import SendFirstPage,SendSecondPage
import time 
#发送首营第一步页面

class SendFirstLinkParameters:

    def set_values(self,all_url,unexchanged_url,file_kinds=1):
        self.file_kinds = file_kinds
        self.all_url = all_url
        self.unexchanged_url = unexchanged_url


class SendFirstLink:
    def __init__(self,sendFirstLinkParameters):
        self.file_kinds = sendFirstLinkParameters.file_kinds
        self.all_url = sendFirstLinkParameters.all_url
        self.unexchanged_url = sendFirstLinkParameters.unexchanged_url

    def execute_page(self,driver,target_company,target_name,cook):
        time.sleep(1)
        sendFirst = SendFirstPage(driver)
        sendFirst.click_class(self.file_kinds)
        time.sleep(1)

        sendFirst.search(target_company)
        time.sleep(2)

        receive_company_data = sendFirst.receive_company_data
        print('data',receive_company_data)
        send_SecondPage = SendSecondPage(driver,cook,receive_company_data)
        send_SecondPage.second(self.all_url,self.unexchanged_url,target_name)



