from selenium import webdriver
from requests_html import HTML
import time
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
import re

base_url = 'http://127.0.0.1'
username = 'admin'
password = 'a69a0d11'

wp = Client(str(base_url)+'/xmlrpc.php',str(username),str(password))
post = WordPressPost()

# 文章发布状态 draft：草稿、publish：发布、private：私密
post.post_status = 'publish'

# wordpress分类
post.terms_names = {
    'category':['旅行商城']
}

# 定义wordpress字段
post.custom_fields = []

def downhtml(url):
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(3) #等待3秒加载js
    html = HTML(html=browser.page_source) # 返回的 page_source 转换成 requests-html 支持的格式
    browser.quit()
    return html

def fabu(url):
    html = downhtml(url)

    # 标题
    title = html.xpath('//h1[@class="title-txt"]/span[1]/text()')[0]
    print(title)
    post.title = title

    # 标题上的小标签
    type_list = html.xpath('//h1[@class="title-txt"]//span[@class="title-tag"]/text()')
    type = ''
    for i in type_list:
        type = str(type) + '\n' + str(i)
    type = re.sub(r'^\n','',type)
    print(type)
    post.custom_fields.append({
        'key':'type',
        'value':type
    })

    # 卖点
    maidian_list = html.xpath('//div[@class="item-subtitle-wrap"]/ul//li/text()')
    maidian = ''
    for i in maidian_list:
        maidian = str(maidian) + '\n' +str(i)
    maidian = re.sub(r'^\n', '', maidian)
    print(maidian)
    post.custom_fields.append({
        'key':'maidian',
        'value':maidian
    })

    # 原价
    yuanjia_list = html.xpath('//div[@class="item-price"]/div[@class="price-items"]/dl[@class="price-dl"]/dd[@class="price-content"][1]//text()')
    yuanjia = ''
    for i in yuanjia_list:
        yuanjia = str(yuanjia) + str(i)
    print(yuanjia)

    # 现价
    xianjia_list = html.xpath('//div[@class="item-price"]/div[@class="price-items"]/dl[@class="price-dl"]/dd[@class="price-content"][2]//text()')
    xianjia = ''
    for i in xianjia_list:
        xianjia = str(xianjia)+str(i)
    print(xianjia)

    # 返回文章ID
    # post.id = wp.call(posts.NewPost(post))
    # print(str(base_url) + '/?p=' + str(post.id))

fabu('https://traveldetail.fliggy.com/item.htm?spm=181.7621407.a1z9b.6.77ca1e3a1fi35e&id=546636958919&scm=20140635.1_1_2.0.0b83e0e715280164660381559e1a9b')