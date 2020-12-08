from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from tqdm import tqdm
import random
import time
import csv

chrome_driver = 'C:/Program Files/Google/Chrome/Application/chromedriver.exe'
browser = webdriver.Chrome(executable_path=chrome_driver)  # 创建一个浏览器对象,这里还可以使用chrome等浏览器
csvheader = ['主营业务','股票代码','股票简称','详细','研报','股吧','申购代码','发行总数（万股）','网上发行（万股）','顶格申购需配市值(万元)',
             '申购上限(万股)','发行价格','最新价','首日收盘价','申购日期（月-日）','申购日期（星期）','中签号公布日','中签交款日期','上市日期','发行市盈率',
             '行业市盈率','中签率','询价累计报价倍数','配售对象报价家数','连续一字板数量','涨幅%','每中一签获利（元）','招股说明书']


def replacement(text):
    import re
    partten = '<[t][d]>\&[n][b][s][p]\;<[\/][t][d]>'
    text = text.replace(u'<td>&nbsp;</td>',u'<td>NAN</td>')
    text = text.replace(u'<td></td>',u'<td>NAN</td>')
    return text


# result_list = []

try:
    browser.get('http://data.eastmoney.com/xg/xg/default.html') # 获取并打开url
    with open('new_stock.csv','a+',newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(csvheader)
        for r in tqdm(range(1,50)):
            html = browser.page_source  # 获取html页面
            # html.replace(u'\xa0', u' ')
            html = replacement(html)
            # print(html)
            doc = pq(html)              # 解析html
            table = doc('.content table')  # 定位到表格
            table.find('script').remove()  # 除去script标签
            table.find('thead').remove()
            list_cont = table('tr').items()  # 获取tr标签列表
            for i in list_cont:
                temp = []
                title = i.attr('title')
                temp.append(title)
                univ = (i.text()).split()  # 获取每个tr标签中的文本信息，返回一个列表
                # print(temp + univ)
                writer.writerow(temp + univ)
            nextpagebutton = browser.find_element_by_xpath('//a[contains(text(),"下一页")]')  # 定位到“下一页”按钮
            nextpagebutton.click()  # 模拟点击下一页
            wait = WebDriverWait(browser, 10)  # 浏览器等待10s
            sec = [2,3,4,5]
            time.sleep(random.choice(sec))
finally:
    browser.close()  # 关闭浏览器
