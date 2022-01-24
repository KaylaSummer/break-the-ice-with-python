from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import re
from lxml import html, etree
from selenium import webdriver
import sqlite3
import os


USERNAME = "13917359700"
PASSWORD = "lgjew9h8"

FUNDCODE = [

"HF0001N97B",
"HF0001MCUU",
"HF0001I31R",
"HF000177PC",
"HF00007E60",
"HF00007BJD",
"HF000073HH",
"HF000071X5",
"HF00006XK6",
"HF00006VB0",
"HF00006VAZ",
"HF00006UEL",


]









#反爬
def getHideIds(htmlEtree):
    encode_styles = "".join(htmlEtree.xpath('//div[@id="ENCODE_STYLE"]/style/text()')).replace("\n", "")
    new_encode_styles = re.sub("  +", "", encode_styles)
    hideIds1 = re.findall("\.(\w+) {font: 0/0 a;", new_encode_styles)
    hideIds2 = re.findall("\.(\w+){font: 0/0 a;", new_encode_styles)
    result = set(hideIds1 + hideIds2)
    # print(result)
    return result

driver = webdriver.Chrome()
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{
    "source":"""
    Object.defineProperty(navigator, 'webdriver', {
        get:() =>undefined
    })
    """
})
driver.get('http://www.simuwang.com/user/option') #登陆

time.sleep(3)
driver.find_element(By.XPATH, '//button[@class="comp-login-method comp-login-b2"]').click()
driver.find_element(By.XPATH,'//input[@name="username"]').send_keys(USERNAME)
driver.find_element(By.XPATH,'//input[@type="password"]').send_keys(PASSWORD)
driver.find_element(By.XPATH,'//button[@style="margin-top: 65px;"]').click()
time.sleep(3)

for each_fund in FUNDCODE():
    each_code = each_fund
    print("开始获取[{name}]的历史净值...".format(name=each_code))

    url = "https://dc.simuwang.com/product/{code}.html".format(code=each_code)

    driver.get(url)
    driver.find_element(By.XPATH, '//div/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/a[2]').click()

    # for i in range(100):
    #     js = 'document.getElementsByClassName("tbody")[0].scrollTop=100000'
    #     driver.execute_script(js)
    #     time.sleep(0.1)

    page_url=driver.page_source
    bs_text = BeautifulSoup(page_url,'html.parser')
    cmpp_fund_name = bs_text.find('h1',class_='line1-title-name ellipsis').get_text()

    # cmpp_fund_code = bs_text.find('span',class_='line4-baseinfo-value ellipsis').get_text()
    
    htmlEtree = etree.HTML(text=page_url)
    hideIds=getHideIds(htmlEtree)
    divList = htmlEtree.xpath('//div[@class="tr flex-h-center"]')
之前都在读数据
    
    date = []
    nav = []
    cum_nav = []
    adj_nav =[]

    df_warehouse_nav = pd.DataFrame(columns=('date','nav','cumnav'))

    for div in divList:
        nextDivs = div.xpath('./div[@class="td flex-h-center"]')
        for nextDiv in nextDivs:      
            if nextDivs.index(nextDiv) == 0:
                date.append(nextDiv.xpath("./text()")[0])
            else:
                labels = nextDiv.xpath("./*")
                nowResultList = []
                for label in labels:
                    classStr = label.xpath("./@class")[0]
                    if classStr not in hideIds:
                        nowResultList.append(label.xpath("./text()")[0])
                # print(nowResultList)
                if nextDivs.index(nextDiv) == 1:
                    nav.append("".join(nowResultList))
                elif nextDivs.index(nextDiv) == 2:
                    cum_nav.append("".join(nowResultList))
                elif nextDivs.index(nextDiv) == 3:
                    adj_nav.append("".join(nowResultList))
    
    dict = {
        "date":date,
        "nav":nav,
        "cum_nav":cum_nav,
    }
    df = pd.DataFrame(dict)

    df['source']   =  "smpp"
    df['name']     =  cmpp_fund_name
    df["code"]     =  each_code
    
    df = df[["code","name","date","nav","cumnav","source"]]

    print(df)
    df.to_excel('~/Desktop/df.xlsx',index = False)
    print('已写入[{name}]私募排排净值数据……'.format(name=cmpp_fund_name))
    # break

driver.quit()