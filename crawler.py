import requests
import time
import pandas as pd
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.support.select import Select #下拉清單
from tqdm import tqdm

#chrome_driver設定
chrome_path = "C:\selenium_driver_chrome\chromedriver.exe" #chromedriver.exe執行檔所存在的路徑


driver = webdriver.Chrome(chrome_path)
data_final = pd.DataFrame()
for l in range(1,210):

    for k in range(2,12):
        driver.get('https://consumer.fda.gov.tw//Food/TFND.aspx?nodeID=178&p={}#ctl00_content_ListPanelinputs_first'.format(l))
        print("page:",l)

        inputs_second = driver.find_element_by_xpath('//*[@id="ctl00_content_ListPanel"]/table/tbody/tr[{}]/td[3]/a'.format(k)).get_attribute('href')
        driver.get(inputs_second)

        base = []
        for i in range(1,9):
            base.append( driver.find_element_by_xpath('//*[@id="ctl00_bgStyle"]/div[2]/div/div/ul/li[{}]/p[2]'.format(i)).text )
        base = pd.DataFrame(base).T
        base.columns = ['食品分類','資料類別','整合編號','樣品名稱','俗名','樣品英文名稱','內容物描述','廢棄率']


        data_sum = pd.DataFrame()
        for j in range(2,105):
            data = []
            for i in range(2,5):
                data.append( driver.find_element_by_xpath('//*[@id="ctl00_bgStyle"]/div[2]/div/table/tbody/tr[{}]/td[{}]'.format(j,i)).text )
            data = pd.DataFrame(data).T
            data.columns = ['分析項','單位','每100克含量']
            data_sum = pd.concat([data_sum,data],axis=0)
            print(base.iat[0,3],"_",data.iat[0,0])

        data_sum['colnames'] = data_sum[['分析項', '單位']].apply(lambda x: "_".join(x), axis=1)
        data_name = data_sum['colnames'].tolist()
        data_number = pd.DataFrame(data_sum['每100克含量']).T.reset_index().drop(columns=["index"])
        data_number.columns = data_name
        base = pd.concat([base,data_number],axis=1)

        data_final = pd.concat([data_final,base],axis=0,ignore_index=True)
        data_final.to_hdf("E:\nutritionDB\data_nutrition.h5",key='s')