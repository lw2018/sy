#--coding:utf-8--
import json
import time

import requests


class SendFirstPage:
    def __init__(self,driver):
        self.driver = driver
        
        self.medicines = self.driver.find_element_by_id("li-company")    #1 品种
        self.business = self.driver.find_element_by_id("li-business")    #2 企业
        self.contract = self.driver.find_element_by_id("li-contract")    #3 合同
        #self.receive_company_data={}
        

    def click_class(self,file_kinds):
        if file_kinds == 2:
            self.business.click()
        elif file_kinds == 3:
            self.contract.click()
        else:
            self.medicines.click()


    def receive_page_elements(self):
        self.search_input = self.driver.find_element_by_id("search-company")
        self.serch_button = self.driver.find_element_by_id("search-logo1")
        self.receive_companys_xpath = "//*[@id='history-list']/div"

    
    def get_receive_company(self,target_company):
        companys=self.driver.find_elements_by_xpath(self.receive_companys_xpath)
        self.receive_company_data={}     #用于存放目标企业的名称和id等数据
        
        for i in range (len(companys)):
            next_company_tag_xpath = "//*[@id='history-list']/div[%s]" % (i+1)
            next_company_name_xpath = "//*[@id='history-list']/div[%s]/p[1]" % (i+1)   #必须打括号(i+1) 写i+1会报类型错误
            next_company_name=self.driver.find_element_by_xpath(next_company_name_xpath).text

            if next_company_name == target_company:
                receive_company=self.driver.find_element_by_xpath(next_company_tag_xpath)

                self.receive_company_data['name']=next_company_name
                self.receive_company_data['id']=receive_company.get_attribute('data-id')
                time.sleep(2)
                #注意py中目录的写法
                self.driver.get_screenshot_as_file('D:\\daima\\auto_syzljh\\photo\\receive_company.png')
                return receive_company



    def search(self,target_company):
        self.receive_page_elements()

        self.search_input.send_keys(target_company)
        time.sleep(1)
        self.serch_button.click()
        time.sleep(2)
        self.get_receive_company(target_company).click()


class SendSecondPage:
    def __init__(self, driver, cook, receive_company_data, headers):
        self.driver=driver
        self.cook=cook
        self.receive_company_data = receive_company_data
        self.headers = headers

    def handle_cook(self,cook):
        for j in cook:
        #根据cook名字只是筛选 united-id csrftoken sessionid 三个cook出来
            if j.get("name")  in ["Hm_lvt_c7a77eff2e8cc0670fac6dec780dbd7a"\
            ,"Hm_lpvt_c7a77eff2e8cc0670fac6dec780dbd7a"]:
                cook.remove(j)
        
        jar=requests.cookies.RequestsCookieJar()
        for i in range(3):
            jar.set(cook[i]['name'],cook[i]['value'],domain=cook[i]['domain'],path=cook[i]['path'])
        return  jar

    def get_all_material(self,url):
        resp=requests.get(url=url,cookies=self.cook)

        materials_data_details=[]
        resp_text=json.loads(resp.text) #json转化为py
        
        self.d_cook=requests.utils.dict_from_cookiejar(self.cook)
        print('self_cook',type(self.cook))
        print('d-cook',type(self.d_cook))
        print("all_cook",self.d_cook)
        
        self.token=self.d_cook.get("csrftoken")
        print('token',self.token)
        """
        for cok in self.cookk:
            if cok.get("name") == "csrftoken":
                self.token = cok.get("value")
                print('token',self.token)
                break
        """

        for i in resp_text.get("results"):
            material_singal_data={}
            material_singal_data["name"]=i.get("name")
            material_singal_data["uuid"]=i.get("uuid")
            materials_data_details.append(material_singal_data)
        
        self.materials_data =\
        {'count':resp_text.get("count"),\
        'details':materials_data_details}
        
    def get_unexchanged_material(self,unexchanged_url,target_name=''):
        #SendFirstPage的变量
        print('data3',self.materials_data)
        unexchanged_materials = []
        """
        headers={\
        "accept": "*/*",\
        "accept-encoding": "gzip, deflate, br",\
        "accept-language": "zh-CN,zh;q=0.9",\
        "cache-control": "no-cache",\
        "content-length": "91",\
        "content-type": "application/json",\
        #"origin": "https://.com",\
        "pragma": "no-cache",\
        #"referer": "https",\
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) Chrome/69.0.3497.92",\
        "x-csrftoken": self.token,\
        "x-requested-with":"XMLHttpRequest"}
        """

        self.headers["x-csrftoken"] = self.token    #必须修改token值
        for material_singal in self.materials_data.get("details"):
            material_uuid=material_singal.get("uuid")
            payload={"is_exchange":"is_material",\
            "receiver_id":self.receive_company_data.get("id"),\
            "uuid":material_uuid}
            
            
            resp=requests.post(unexchanged_url, data=json.dumps(payload), headers=self.headers, cookies=self.cook)
            if resp.status_code == 200:
                print('data200',json.loads(resp.text))

            else:
                print('data',resp.status_code)

            print('data5',resp.text)
            if resp.status_code == 200 and\
            json.loads(resp.text).get("data").get("exchanged") == False:
                unexchanged_materials.append(material_singal)
                print('data4',json.loads(resp.text))
            time.sleep(1)
        #print('data5',resp)
        print('data2',unexchanged_materials)
        if target_name == '':
            self.unexchanged_material = unexchanged_materials[0].get('name')
        else:
            self.unexchanged_material = target_name
        
    def SendSecondPage_elements(self):
        self.search_input = self.driver.find_element_by_id('search-product')
        self.search_button = self.driver.find_element_by_id('search-logo2')
        self.next_step_button = self.driver.find_element_by_id('next-step-three')
        self.send_material_xpath = '//*[@id="drug"]/table/tbody/tr[1]/td[1]/input'

    def get_data(self,all_url,unexchanged_url,target_name):
        #self.handle_cook(cook)
        self.get_all_material(all_url)
        time.sleep(1)
        self.get_unexchanged_material(unexchanged_url,target_name)
        #可能还要处理 targe_name参数

    def second(self,all_url,unexchanged_url,target_name):
        self.get_data(all_url,unexchanged_url,target_name)
        self.SendSecondPage_elements()

        self.search_input.send_keys(self.unexchanged_material)
        self.search_button.click()
        time.sleep(2)

        self.send_material_input = self.driver.find_element_by_xpath(self.send_material_xpath)
        self.send_material_input.click()
        time.sleep(1)

        self.next_step_button.click()
