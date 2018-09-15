#--coding:utf-8--
from SendLast import SendLastPage

class SendLastLink():
    def execute_page(self,driver):
        send_LastPage = SendLastPage(driver)
        send_LastPage.last()

