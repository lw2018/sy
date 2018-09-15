#--coding:utf-8--
from selenium.common.exceptions import StaleElementReferenceException
import time

class SendLastPage:
    def __init__(self,driver):
        self.driver = driver
    
    def lastPage_StaticElements(self):
        #委托书
        #self.upload_proxy_tag=self.driver.find_element_by_id('upload-layer')
        #发送按钮
        self.send_button=self.driver.find_element_by_id('comfirm-submit')

        #品种资料
        self.matched_product_documents=self.driver.find_elements_by_xpath('//*[@id="matched-product-checked-file"]/button')
        self.unmatched_product_documents=self.driver.find_elements_by_xpath('//*[@id="unmatched-product-checked-file"]/button')
        
        #生产企业资料
        self.matched_main_company_documents=self.driver.find_elements_by_xpath('//*[@id="matched-main-checked-file"]/button')
        self.unmatched_main_company_documents=self.driver.find_elements_by_xpath('//*[@id="unmatched-main-checked-file"]/button')
        
        #关联企业资料文件夹元素
        self.matched_sub_company_documents=self.driver.find_elements_by_xpath('//*[@id="matched-sub-checked-file"]/button')
        self.unmatched_sub_company_documents=self.driver.find_elements_by_xpath('//*[@id="unmatched-sub-checked-file"]/button')
    
    def document_DynamicElements(self):
        self.all_checkbox_input=self.driver.find_element_by_name('all-checkbox')
        self.select_ok_tag=self.driver.find_element_by_class_name('layui-layer-btn0')
        self.single_files=self.driver.find_elements_by_name('sub-checkbox')
    
    def upload_proxy_StaticElement(self):
        self.upload_proxy_tag = self.driver.find_element_by_id('upload-layer')
    
    def local_upload_DynamicElement(self):
        self.local_upload_tag=self.driver.find_element_by_id('local-upload')

    def upload_proxyFile_DynamicElement(self):
        self.upload_proxyFile_input=self.driver.find_element_by_id('add-file-input')
        self.upload_ok=self.driver.find_element_by_xpath('//*[@id="layui-layer2"]/div[3]/a[2]')

    def get_data(self):
        self.lastPage_StaticElements()
        product_documents = self.matched_product_documents + self.unmatched_product_documents
        main_company_documents = self.matched_main_company_documents + self.unmatched_main_company_documents
        sub_company_documents = self.matched_sub_company_documents + self.unmatched_sub_company_documents
        #所有要发送的品种+企业资料
        all_send_document=[]
        all_send_document.append(product_documents[0:2])
        all_send_document.append(main_company_documents[0:2])
        all_send_document.append(sub_company_documents[0:2])
        ##删除所有要发送资料其中的空资料
        while [] in all_send_document:
            all_send_document.remove([])
        self.all_send_document = all_send_document

        all_send_documents_lenList=[]
        for documents_list in all_send_document:
            all_send_documents_lenList.append(len(documents_list))
        self.all_send_documents_lenList = all_send_documents_lenList
        print("要发送的各排文件的长度",self.all_send_documents_lenList)

        #所有的不发送品种和企业资料
        all_unsend_document=[]
        all_unsend_document.append(product_documents[2:len(product_documents)])
        all_unsend_document.append(main_company_documents[2:len(main_company_documents)])
        all_unsend_document.append(sub_company_documents[2:len(sub_company_documents)])
        ##删除所有资料其中的空资料
        while [] in all_unsend_document:
            all_unsend_document.remove([])
        self.all_unsend_document = all_unsend_document

        all_unsend_documents_lenList=[]
        for documents_list in all_unsend_document:
            all_unsend_documents_lenList.append(len(documents_list))
        self.all_unsend_documents_lenList = all_unsend_documents_lenList
        print("不发送的各排文件的长度",self.all_unsend_documents_lenList)


    def upload_proxy(self):         #基于大页面具体的小页面 函数命名不够直白 继续改
        self.upload_proxy_StaticElement()
        self.upload_proxy_tag.click()
        time.sleep(1)

        self.local_upload_DynamicElement()
        self.local_upload_tag.click()
        time.sleep(2)

        self.upload_proxyFile_DynamicElement()
        self.upload_proxyFile_input.send_keys('D:\\tu\\proxy\\back.jpg')
        time.sleep(3)

        self.upload_ok.click()

    #药品和企业
    def upload_none_proxy(self):
        self.get_data()
        #要发送的
        for j in range(len(self.all_send_document)):
        #for company_or_product_documents in all_document:
            #current_documents=company_or_product_documents
            #for i in range(2):
            for i in range(self.all_send_documents_lenList[j]):
            
                attempts=0
                while attempts<2:
                    #self.lastPage_StaticElements()
                    self.get_data()
                    print('j:',j)
                    print("i:",i)
                    current_ducument=self.all_send_document[j][i]
                    
                    
                    try:
                        current_ducument.click()  #单个文件夹点击展开
                                ##全选框的处理 让任何文件都没有处于选中状态
                        time.sleep(1)
                        print(888)
                        
                        self.document_DynamicElements()
                        is_select = self.all_checkbox_input.is_selected()
                        if is_select==False:
                            self.all_checkbox_input.click()
                            time.sleep(1)
                            self.all_checkbox_input.click()
                        else:
                            self.all_checkbox_input.click()
                                    
                                #根据选择框的个数判断每个文件夹里面文件的个数
                            time.sleep(1)
                            #single_files=self.driver.find_elements_by_name('sub-checkbox')
                            
                        if len(self.single_files)<3:  #每个文件夹1到2个文件
                            self.all_checkbox_input.click()
                        else:   #文件夹里面的文件多余2个 则只是选中前面2个
                                print(999)
                                is_select_count=0
                                for single_file in self.single_files:
                                    single_file.click()
                                    is_select_count+=1
                                    time.sleep(1)
                                    if is_select_count==2:
                                        break
                            
                            
                        time.sleep(1)
                        self.select_ok_tag.click()   #每个具体文件选择框点击确定
                        print(000)

                        time.sleep(3)
                        break
                    except StaleElementReferenceException as e:
                            print(e)
                            #self.lastPage_StaticElements()
                            attempts += 1
                            time.sleep(2)
                            print("retry")


        print("下面是不发送的----------")
        if len(self.all_unsend_document) !=0:
            for j in range(len(self.all_unsend_document)):
                for i in range(self.all_unsend_documents_lenList[j]):
            
                    attempts=0
                    while attempts<2:
                        #self.lastPage_StaticElements()
                        self.get_data()
                        print('j:',j)
                        print("i:",i)
                        current_ducument=self.all_unsend_document[j][i]
                        
                        
                        try:
                            current_ducument.click()  #单个文件夹点击展开
                                    ##全选框的处理 让任何文件都没有处于选中状态
                            time.sleep(1)
                            print(888)
                            
                            self.document_DynamicElements()
                            is_select = self.all_checkbox_input.is_selected()
                            if is_select==False:
                                self.all_checkbox_input.click()
                                time.sleep(1)
                                self.all_checkbox_input.click()
                            else:
                                self.all_checkbox_input.click()
                            time.sleep(1)
                            self.select_ok_tag.click()   #每个具体文件选择框点击确定
                            print(000)

                            time.sleep(3)
                            break
                        except StaleElementReferenceException as e:
                                print(e)
                                #self.lastPage_StaticElements()
                                attempts += 1
                                time.sleep(2)
                                print("retry_unsend")
 

        """
        #所有不发送文件保持未选中状态
        if len(self.all_unsend_document) !=0:
            for unsend_documents in self.all_unsend_document:
                for  unsend_document in unsend_documents:
                    attempts=0
                    while attempts<2:
                        self.lastPage_StaticElements()
                        current_document=unsend_document
                        try:
                                current_document.click()  #单个文件夹点击展开
                                        ##全选框的处理 让任何文件都没有处于选中状态
                                time.sleep(1)
                                print(201)
                                
                                self.document_DynamicElements()
                                is_select=self.all_checkbox_input.is_selected()
                                if is_select==False:
                                    self.all_checkbox_input.click()
                                    time.sleep(1)
                                    self.all_checkbox_input.click()
                                else:
                                    self.all_checkbox_input.click()
                                self.select_ok_tag.click()
                                time.sleep(2)
                                break
                        except StaleElementReferenceException as e:
                            print(e)
                            self.lastPage_StaticElements()
                            attempts += 1
                            time.sleep(2)
        """
    def last(self):
        self.upload_proxy()
        time.sleep(1)

        self.upload_none_proxy()
        time.sleep(2)

        #self.send_button.click() #确定发送
        print("完成")
        self.driver.get_screenshot_as_file('D:\\daima\\auto_syzljh\\photo\\send_before.png')
        time.sleep(2)
        
      


        









    