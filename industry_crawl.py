from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from tqdm import tqdm
import random
import time
import csv
import pandas as pd
import re

chrome_driver = 'C:/Program Files/Google/Chrome/Application/chromedriver.exe'
browser = webdriver.Chrome(executable_path=chrome_driver)  # 创建一个浏览器对象
csvheader = ['stock_code','stock_name','industry']

f = pd.read_csv('./new_stock.csv', na_values='NAN',encoding='gbk')
f = f[['股票代码','股票简称']]


def code_fill(x):
    x = str(x)
    while len(x) < 6:
        x = '0' + x
    return x


f['股票代码'] = f['股票代码'].apply(lambda x: code_fill(x))


try:
    with open('stock_industry.csv', 'a+', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(csvheader)
        with tqdm(total=f.shape[0], desc='Example', leave=True, ncols=100, unit='B', unit_scale=True) as pbar:
            for index, row in f.iterrows():
                url = 'http://data.eastmoney.com/stockdata/' + row['股票代码'] + '.html'
                browser.get(url)  # 获取并打开url
                extendbutton = browser.find_element_by_xpath("//div[@class='btn-bottom']")
                extendbutton.click()  # 点击延伸按钮
                html = browser.page_source  # 获取html页面
                # print(html)
                doc = pq(html)              # 解析html
                table = doc(".hxtc-content")
                list_cont = table('b').items()
                n = 1
                for i in list_cont:
                    if n == 4:
                        univ = re.findall('(?<=<b>)(.*)(?=</b>)',str(i))
                        writer.writerow([row['股票代码'],row['股票简称'],univ[0]])
                        break
                    n += 1
                wait = WebDriverWait(browser, 10)  # 浏览器等待10s
                sec = [0.5,1,2]
                time.sleep(random.choice(sec))
                pbar.update(1)
finally:
    browser.close()  # 关闭浏览器
