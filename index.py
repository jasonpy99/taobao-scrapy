from selenium import webdriver
from requests_html import HTML
import time
from wordpress_xmlrpc import Client, WordPressPost
import re

base_url = 'http://127.0.0.1'
username = 'admin'
password = '1990101'

wp = Client(str(base_url)+'/xmlrpc.php',str(username),str(password))
post = WordPressPost()

# 文章发布状态 draft：草稿、publish：发布、private：私密
post.post_status = 'publish'

# wordpress分类
post.terms_names = {
    'category':['旅行商城']
}

def downhtml(url):
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(10) #等待10秒加载js
    html = HTML(html=browser.page_source) # 返回的 page_source 转换成 requests-html 支持的格式
    browser.quit()
    return html

def fabu(url):
    html = downhtml(url)

    # 定义wordpress字段
    post.custom_fields = []

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
    yuanjia_list = html.xpath('//dd[@class="price-content"][1]//text()')
    yuanjia = ''
    for i in yuanjia_list:
        yuanjia = str(yuanjia) + str(i)
    print(yuanjia)
    post.custom_fields.append({
        'key':'yuanjia',
        'value':yuanjia
    })

    # 现价
    xianjia = html.find('.big-price span')[0].text
    xianjia = '¥'+str(xianjia)
    print(xianjia)
    post.custom_fields.append({
        'key':'xianjia',
        'value':xianjia
    })

    info_list = html.find('li.item-desc-item')
    for i in info_list:
        title = i.find('.item-desc-title')[0].text
        if '出发地' in title:
            chufadi_list = i.find('.item-desc-content span')
            chufadi=''
            for i in chufadi_list:
                chufadi = str(chufadi)+'\n'+str(i.text)
            chufadi = re.sub(r'^\n','',chufadi)
            print(chufadi)
            post.custom_fields.append({
                'key':'chufadi',
                'value':chufadi
            })
        if '目的地' in title:
            mudidi_list = i.find('.item-desc-content span')
            mudidi = ''
            for i in mudidi_list:
                mudidi = str(mudidi)+'\n'+str(i.text)
            mudidi = re.sub(r'^\n', '', mudidi)
            print(mudidi)
            post.custom_fields.append({
                'key':'mudidi',
                'value':mudidi
            })
        if '行程天数' in title:
            xingchengtianshu_list = i.find('.item-desc-content span')
            xingchengtianshu = ''
            for i in xingchengtianshu_list:
                xingchengtianshu = str(xingchengtianshu)+str(i.text)
            print(xingchengtianshu)
            post.custom_fields.append({
                'key':'xingchengtianshu',
                'value':xingchengtianshu
            })
        if '商品包含' in title:
            shangpinbaohan_list = i.find('.item-desc-content span')
            shangpinbaohan = ''
            for i in shangpinbaohan_list:
                shangpinbaohan = str(shangpinbaohan)+'\n'+str(i.text)
            shangpinbaohan = re.sub(r'^\n','',shangpinbaohan)
            print(shangpinbaohan)
            post.custom_fields.append({
                'key':'shangpinbaohan',
                'value':shangpinbaohan
            })
        if '服务承诺' in title:
            fuwuchengnuo_list = i.find('.item-desc-content span')
            fuwuchengnuo = ''
            for i in fuwuchengnuo_list:
                fuwuchengnuo = str(fuwuchengnuo)+'\n'+str(i.text)
            fuwuchengnuo = re.sub(r'^\n','',fuwuchengnuo)
            print(fuwuchengnuo)
            post.custom_fields.append({
                'key':'fuwuchengnuo',
                'value':fuwuchengnuo
            })

    st_list = html.find('.item-gallery-bottom li img')

    try:
        st_list[0].attrs['src']
    except:
        pass
    else:
        st1 = st_list[0].attrs['src']
        st1 = re.sub('_64x64.jpg','',st1)
        print(st1)
        post.custom_fields.append({
            'key':'st1',
            'value':st1
        })

    try:
        st_list[1].attrs['src']
    except:
        pass
    else:
        st2 = st_list[1].attrs['src']
        st2 = re.sub('_64x64.jpg','',st2)
        print(st2)
        post.custom_fields.append({
            'key':'st2',
            'value':st2
        })

    try:
        st_list[2].attrs['src']
    except:
        pass
    else:
        st3 = st_list[2].attrs['src']
        st3 = re.sub('_64x64.jpg','',st3)
        print(st3)
        post.custom_fields.append({
            'key':'st3',
            'value':st3
        })

    try:
        st_list[3].attrs['src']
    except:
        pass
    else:
        st4 = st_list[3].attrs['src']
        st4 = re.sub('_64x64.jpg','',st4)
        print(st4)
        post.custom_fields.append({
            'key':'st4',
            'value':st4
        })

    try:
        st_list[4].attrs['src']
    except:
        pass
    else:
        st5 = st_list[4].attrs['src']
        st5 = re.sub('_64x64.jpg','',st5)
        print(st5)
        post.custom_fields.append({
            'key':'st5',
            'value':st5
        })

    # 返回文章ID
    # post.id = wp.call(posts.NewPost(post))
    # print(str(base_url) + '/?p=' + str(post.id))

fabu('https://traveldetail.fliggy.com/item.htm?spm=181.7621407.a1z9b.6.77ca1e3a1fi35e&id=546636958919&scm=20140635.1_1_2.0.0b83e0e715280164660381559e1a9b')