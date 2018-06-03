from selenium import webdriver
from requests_html import HTMLSession
from requests_html import HTML
import time

def downhtml(url):
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(3)
    # 返回的 page_source 转换成 requests-html 支持的格式
    html = HTML(html=browser.page_source)
    browser.quit()
    return html

def fabu(url):
    html = downhtml(url)

    title = html.xpath('//h1[@class="title-txt"]/span[1]/text()')[0]
    print(title)

fabu('https://traveldetail.fliggy.com/item.htm?id=543815490670')