#--coding:utf-8--
import json
import time
import traceback

from HomePageLink import HomePageLink, HomePageLinkParameters
from LoginLink import LoginLink, LoginLinkParameters
from selenium import webdriver
from SendFirstLink import SendFirstLink, SendFirstLinkParameters
from SendLastLink import SendLastLink

#find_element 没找到会报异常 find_elements不会 只是会给一个空
"""
def handle_cook(cook):
        
        for j in cook:
        #根据cook名字只是筛选 united-id csrftoken sessionid 三个cook出来
            if j.get("name")  in\
            ["Hm_lvt_c7a77eff2e8cc0670fac6dec780dbd7a",\
            "Hm_lpvt_c7a77eff2e8cc0670fac6dec780dbd7a"]:
                cook.remove(j)
        
        
        print(type(cook))
        print('s_cook',cook)
        jar=requests.cookies.RequestsCookieJar()
        for i in range(3):
            #jar.set(cook[i]['name'],cook[i]['value'],domain=cook[i]['domain'],path=cook[i]['path'])
            jar.set(cook[i]['name'],cook[i]['value'])

        return jar 
"""


if __name__=="__main__":
    #选择要登录的帐号(谷歌)

    driver = webdriver.Chrome()
    target_line = 1
    with  open('..\\setting\\data.json',encoding='utf-8') as f:
        data=json.load(f)
        username = data.get('user_data').get('%d' % target_line)[0]
        password = data.get('user_data').get('%d' % target_line)[1]
        verify_code = data.get('user_data').get('%d' % target_line)[2]
        url = data.get('web_data').get('url')[0]
        all_url = data.get('web_data').get('all_url')[0]
        unexchanged_url = data.get('web_data').get('unexchanged_url')[0]
        company = data.get('company')[0]
        product = data.get('product')[0]
        headers = data.get('headers')

    """
    with open('account.txt','r',encoding='utf-8') as total:

        target_line=5        #根据账号所在行数来更改,不同的行数代表不同的帐号数据
        line_number=1
        for each_line in total:
            if line_number == target_line:
                username,password,verify_code = each_line.split(',')
                break
            line_number += 1
    """
    
    
    print("""前端不行后端来 后端不行结合着来. 机器不行人来.
    都不行,施主 一切讲究个缘字 人生如梦如戏""")
    try:
        #登陆场景
        loginLinkParameters = LoginLinkParameters()
        loginLinkParameters.set_values(url,username,password,verify_code)
        loginLink = LoginLink(loginLinkParameters)
        loginLink.execute_page(driver)
        #cook_jar = handle_cook(driver.get_cookies())
        cook_jar = loginLink.jar
        
        
        
        #登录后侧边栏选择
        homePageLinkParameters = HomePageLinkParameters()
        homePageLinkParameters.set_values()
        homePageLink= HomePageLink(homePageLinkParameters)
        homePageLink.execute_page(driver)

        #发送首营业第一步 品种 企业 合同    第二步选择资料 
        sendFirstLinkParameters = SendFirstLinkParameters()
        sendFirstLinkParameters.set_values(all_url, unexchanged_url, headers)
        sendFirstLink = SendFirstLink(sendFirstLinkParameters)
        sendFirstLink.execute_page(driver, company, product, cook_jar)

        #发送最后一步
        send_LastLink=SendLastLink()
        send_LastLink.execute_page(driver)
        
    except:
        traceback.print_exc()
    finally:
        
        time.sleep(2)
        driver.quit()
