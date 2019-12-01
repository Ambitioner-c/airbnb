
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import re
from bs4 import BeautifulSoup
from random import randint
from time import sleep
import requests
import chardet
import json


# 配置驱动
chrome_opt = Options()  # 创建参数设置对象.
chrome_opt.add_argument('--headless')  # 无界面化.
# chrome_opt.add_argument('--disable-gpu')  # 配合上面的无界面化.
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_opt.add_experimental_option("prefs", prefs)  #不加载图片
chrome_opt.add_argument('--window-size=1366,768')  # 设置窗口大小, 窗口大小会有影响.
# chrome_opt.add_argument("--no-sandbox") #使用沙盒模式运行

# 创建Chrome对象并传入设置信息.
driver = webdriver.Chrome(executable_path='/home/cfl/chromedriver/chromedriver', chrome_options=chrome_opt)


# doc = open(r'../data/test.html', 'w')
# 爬取
url = 'https://www.airbnb.com/rooms/18363560'

driver.get(url)
# 设置超时等待
WebDriverWait(driver,50,0.5).until(lambda x:x.find_element_by_id('summary'))

html = driver.page_source
# print(html, file=doc)

html = BeautifulSoup(html, 'lxml')

# 房屋图片src
room_picture_div_generator = html.findAll('meta', attrs={'itemprop': 'image'})[0].next_siblings
for i in room_picture_div_generator:
    room_picture_div = i
room_picture_src_img = room_picture_div.findAll('img')
room_picture_src = []
for i in room_picture_src_img:
    room_picture_src.append(str(i.get('src')).split('?', 1)[0])
print('房屋图片src:%s' % room_picture_src)

# 房间id
room_id = re.findall(r'rooms/(\d+)', url)[0]
print('房间id:%s' % room_id)

# 房主id
room_div = html.findAll('div', attrs={'id': 'summary'})[0]
room_a = room_div.findAll('a', attrs={'href': re.compile(r'/users/show')})[0]
room_owner_id = re.findall(r'/users/show/(\d+)', str(room_a))[0]
print('房主id:%s' % room_owner_id)

# 房主头像src
room_owner_img = room_a.findAll('img')[0]
room_owner_src = str(room_owner_img.get('src')).split('?', 1)[0]
print('房主头像src:%s' % room_owner_src)

# 评论者信息
# reviewers_div = html.findAll('div', attrs={'id': 'reviews'})[0]
# reviewers_a = reviewers_div.findAll('a', attrs={'href': re.compile(r'/users/show')})
reviews_id = []
reviews_rating = []
# 评论id
# reviews_id = re.findall(r'data-review-id="(.+?)"', str(reviewers_div))
# print('评论id:%s' % reviews_id)

reviewers_id = []
reviewers_src = []
# for i in reviewers_a:
#     if re.findall(r'/users/show/(\d+)', str(i))[0] == room_owner_id:
#         continue
#     # 评论者id
#     reviewers_id.append(re.findall(r'/users/show/(\d+)', str(i))[0])
#
#     # 评论者src
#     reviewers_img = i.findAll('img')[0]
#     reviewers_src.append(str(reviewers_img.get('src')).split('?', 1)[0])
# print('评论者id:%s' % reviewers_id)
# print('评论者src:%s' % reviewers_src)

# 导航条
navigation = html.findAll('nav', attrs={'role': 'navigation'})[0]
li = navigation.findAll('li')[len(navigation.findAll('li'))-2]

# 总页数
page = re.findall(r'>(\d+)<', str(li))[0]
for i in range(0, int(page)):
    reurl = 'https://www.airbnb.com/api/v2/homes_pdp_reviews?currency=CNY' \
            '&key=d306zoyjsyarp7ifhu67rjxn52tv0t20' \
            '&locale=en&' \
            'listing_id=%s' \
            '&_format=for_p3' \
            '&limit=7' \
            '&offset=%s' \
            '&order=language_country' % (str(room_id), str(i*7))
    response = requests.get(reurl)
    response.encoding = chardet.detect(response.content)['encoding']
    html = json.loads(response.text)

    # 评论信息
    reviews = html['reviews']
    for i in reviews:
        # 评论id
        reviews_id.append(i['id'])

        # 评论者id
        reviewers_id.append(i['reviewer']['id'])
        # 评论者src
        reviewers_src.append(i['reviewer']['picture_url'])
        # 评论者rating
        reviews_rating.append(i['rating'])
print(len(reviews_id))
print('评论id:%s' % reviews_id)

print(len(reviews_rating))
print('评论rating:%s' % reviews_rating)

print(len(reviewers_id))
print('评论者id:%s' % reviewers_id)

print(len(reviewers_src))
print('评论者src:%s' % reviewers_src)

# doc.close()
driver.close()
