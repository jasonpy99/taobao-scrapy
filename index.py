from selenium import webdriver
from requests_html import HTML
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
import re
import time
import xlrd
import os

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
    time.sleep(5)

    # 返回的 page_source 转换成 requests-html 支持的格式
    html = HTML(html=browser.page_source)
    browser.quit()
    return html

def fabu(url):
    # 定义html
    html = downhtml(url)

    # 飞猪url 写入 fliggy_url 字段
    post.custom_fields.append({
        'key':'fliggy_url',
        'value':url
    })

    # 获取标题
    title = html.xpath('//h1[@class="title-txt"]/span[1]/text()')[0]
    print(title)
    post.title = title

    # 获取类型（跟团游，飞猪专线）
    type_list = html.xpath('//h1[@class="title-txt"]//span[@class="title-tag"]/text()')
    post.custom_fields.append({
        'key': 'type',
        'value': str(type_list)
    })

    # 获取首图 1
    st_list = html.find('//h1[@class="title-txt"]//span[@class="title-tag"]')
    st1 = st_list[0].attrs['src']
    st1 = re.sub('_64x64.jpg', '', st1)
    st1 = 'https:' + str(st1)
    print(st1)
    post.custom_fields.append({
        'key': 'st1',
        'value': st1
    })

    # 获取首图 2
    st2 = st_list[1].attrs['src']
    st2 = re.sub('_64x64.jpg', '', st2)
    st2 = 'https:' + str(st2)
    print(st2)
    post.custom_fields.append({
        'key': 'st2',
        'value': st2
    })

    # 获取首图 3
    st3 = st_list[2].attrs['src']
    st3 = re.sub('_64x64.jpg', '', st3)
    st3 = 'https:' + str(st3)
    print(st3)
    post.custom_fields.append({
        'key': 'st3',
        'value': st3
    })

    # 获取首图 4
    st4 = st_list[3].attrs['src']
    st4 = re.sub('_64x64.jpg', '', st4)
    st4 = 'https:' + str(st4)
    print(st4)
    post.custom_fields.append({
        'key': 'st4',
        'value': st4
    })

    # 获取首图 5
    try:
        st5 = st_list[4].attrs['src']
    except IndexError:
        pass
    else:
        st5 = st_list[4].attrs['src']
        st5 = re.sub('_64x64.jpg', '', st5)
        st5 = 'https:' + str(st5)
        print(st5)
        post.custom_fields.append({
            'key': 'st5',
            'value': st5
        })

    # 获取卖点
    try:
        maidian = html.find('ul.item-subtitle-content', first=True).text
    except AttributeError:
        pass
    else:
        maidian = html.find('ul.item-subtitle-content', first=True).text
        print(maidian)
        post.custom_fields.append({
            'key': 'maidian',
            'value': maidian
        })

    # 获取原价
    yuanjia = html.find('.price-content', first=True).text
    yuanjia = re.sub('¥', '', yuanjia)
    print(yuanjia)
    post.custom_fields.append({
        'key': 'yuanjia',
        'value': yuanjia
    })

    # 获取折扣价
    xianjia = html.find('.big-price span', first=True).text
    print(xianjia)
    post.custom_fields.append({
        'key': 'xianjia',
        'value': xianjia
    })

    # 出发地
    chufadi_list = html.find('ul.item-desc li .item-desc-content')[0]
    chufadi_list = chufadi_list.find('span')
    chufadi = ''
    for i in chufadi_list:
        chufadi = str(i.text) + ',' + chufadi
    chufadi = re.sub(',$', '', chufadi)
    print(chufadi)
    post.custom_fields.append({
        'key': 'chufadi',
        'value': chufadi
    })

    # 目的地
    mudidi_list = html.find('ul.item-desc li .item-desc-content')[1]
    mudidi_list = mudidi_list.find('span')
    mudidi = ''
    for i in mudidi_list:
        mudidi = str(i.text) + ',' + mudidi
    mudidi = re.sub(',$', '', mudidi)
    print(mudidi)
    post.custom_fields.append({
        'key': 'mudidi',
        'value': mudidi
    })

    # 天数
    tianshu_list = html.find('ul.item-desc li .item-desc-content')[2]
    tianshu_list = tianshu_list.find('span')
    tianshu = ''
    for i in tianshu_list:
        tianshu = str(i.text) + ',' + tianshu
    tianshu = re.sub(',$', '', tianshu)
    print(tianshu)
    post.custom_fields.append({
        'key': 'tianshu',
        'value': tianshu
    })

    # 服务承诺
    chengnuo_list = html.find('ul.item-desc li .item-desc-content')[3]
    chengnuo_list = chengnuo_list.find('span')
    chengnuo = ''
    for i in chengnuo_list:
        chengnuo = str(i.text) + ',' + chengnuo
    chengnuo = re.sub(',$', '', chengnuo)
    print(chengnuo)
    post.custom_fields.append({
        'key': 'chengnuo',
        'value': chengnuo
    })

    # 详情页
    xiangqing = html.find('.descr-txt-content', first=True).html
    xiangqing = re.sub('data-ks-lazyload', 'src', xiangqing)
    xiangqing = re.sub(r'(style|data-lazyid|align)="[\s\S]*?"', '', xiangqing)
    xiangqing = re.sub('  ', '', xiangqing)
    xiangqing = re.sub('<div[\s\S]*?>', '', xiangqing)
    xiangqing = re.sub('</div>', '', xiangqing)
    print(xiangqing)
    post.custom_fields.append({
        'key': 'xiangqing',
        'value': xiangqing
    })

    # 行程
    try:
        xingcheng = html.find('.travel-detail', first=True).html
    except AttributeError:
        xingcheng = html.find('#J_Itineraries', first=True).html
        print(xingcheng)
        post.custom_fields.append({
            'key': 'xingcheng',
            'value': xingcheng
        })
    else:
        xingcheng = html.find('.travel-detail', first=True).html
        print(xingcheng)
        post.custom_fields.append({
            'key': 'xingcheng',
            'value': xingcheng
        })

    # 费用包含
    try:
        feiyongbaohan = html.find('.description-txt-wrapper .txt-content')[0].text
    except AttributeError:
        feiyongbaohan = html.find('#J_FeeInclude', first=True).text
        print(feiyongbaohan)
        post.custom_fields.append({
            'key': 'feiyongbaohan',
            'value': feiyongbaohan
        })
    else:
        feiyongbaohan = html.find('.description-txt-wrapper .txt-content')[0].text
        print(feiyongbaohan)
        post.custom_fields.append({
            'key': 'feiyongbaohan',
            'value': feiyongbaohan
        })

    # 费用不含
    try:
        feiyongbuhan = html.find('.description-txt-wrapper .txt-content')[1].text
    except AttributeError:
        feiyongbuhan = html.find('#J_FeeExclude', first=True).text
        print(feiyongbuhan)
        post.custom_fields.append({
            'key': 'feiyongbuhan',
            'value': feiyongbuhan
        })
    else:
        feiyongbuhan = html.find('.description-txt-wrapper .txt-content')[1].text
        print(feiyongbuhan)
        post.custom_fields.append({
            'key': 'feiyongbuhan',
            'value': feiyongbuhan
        })

    # 自费项目
    zifeixiangmu = html.find('.description-txt-wrapper .txt-content')[2].text

    zifeixiangmu_title = html.find('.description-txt-wrapper .desc-title')[2].text
    if str(zifeixiangmu_title) == '自费项目':
        print(zifeixiangmu)
        post.custom_fields.append({
            'key': 'zifeixiangmu',
            'value': zifeixiangmu
        })

    # 预订须知
    try:
        yudingxuzhi = html.find('.description-txt-wrapper .txt-content')[3].text
    except IndexError:
        yudingxuzhi = html.find('#J_BookTips .txt-content', first=True).text
        print(yudingxuzhi)
        post.custom_fields.append({
            'key': 'yudingxuzhi',
            'value': yudingxuzhi
        })
    else:
        yudingxuzhi = html.find('.description-txt-wrapper .txt-content')[3].text
        print(yudingxuzhi)
        post.custom_fields.append({
            'key': 'yudingxuzhi',
            'value': yudingxuzhi
        })

    # 退改规则
    try:
        tuigaiguize = html.find('.description-table-txt-wrapper .txt-content')[0].html
    except AttributeError:
        tuigaiguize = html.find('#J_RefundTerms', first=True).html
        tuigaiguize = re.sub(r'<div[\s\S]*?>', '', tuigaiguize)
        tuigaiguize = re.sub('</div>', '', tuigaiguize)
        tuigaiguize = re.sub(r' class="[\s\S]*?"', '', tuigaiguize)
        print(tuigaiguize)
        post.custom_fields.append({
            'key': 'tuigaiguize',
            'value': tuigaiguize
        })
    else:
        tuigaiguize = html.find('.description-table-txt-wrapper .txt-content')[0].html
        tuigaiguize = re.sub(r'<div[\s\S]*?>', '', tuigaiguize)
        tuigaiguize = re.sub('</div>', '', tuigaiguize)
        tuigaiguize = re.sub(r' class="[\s\S]*?"', '', tuigaiguize)
        print(tuigaiguize)
        post.custom_fields.append({
            'key': 'tuigaiguize',
            'value': tuigaiguize
        })

    # 保险说明
    baoxianshuoming = html.find('.insurance .note-wrap')[0].text
    print(baoxianshuoming)
    post.custom_fields.append({
        'key': 'baoxianshuoming',
        'value': baoxianshuoming
    })

for root,dirs,files in os.walk('c:/excel'):
    for fn in files:
        workbook = xlrd.open_workbook(root+'/'+fn)
        sheet_names = workbook.sheet_names()  #遍历excel表单

        for sheet_name in sheet_names:
            sheet = workbook.sheet_by_name(sheet_name)
            cp_id = sheet.col_values(0)
            for id in range(len(cp_id)):
                if(id != 0):
                    cp_url = 'https://traveldetail.fliggy.com/item.htm?id=' + str(cp_id[id])
                    print(cp_url)
                    fabu(cp_url)
                    post.id = wp.call(posts.NewPost(post))
                    print(str(base_url) + '/?p=' + str(post.id))

