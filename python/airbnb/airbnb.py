# 从网站爬取相关信息，并下载数据到csv
import requests
import chardet
import json
import time
import csv
import os
import threading
import subprocess
from subprocess import run
from time import sleep


def get_network():
    ip = 'www.baidu.com'

    # 执行命令行指令并返回结果
    before = run('ping -c 1 %s' % ip, shell=True, stdout=subprocess.PIPE)

    # 如果返回值是0表示连通，否则为断开
    before_code = before.returncode
    if before_code == 0:

        return
    else:
        data = {'DDDDD': '2016214436', 'upass': '656359504', '0MKKey': '123'}
        requests.post('http://172.16.200.13', data=data)
        print('线程-1联网！')

        return


def get_room_id(pathname):
    # 全列表
    room_all_id = []
    room_all_id_reader = csv.reader(open(pathname + 'room_all_id.csv', 'r'))
    for j in room_all_id_reader:
        room_all_id.append(j)

    # 已完成列表
    room_finish_id = []
    room_finish_reader = csv.reader(open(pathname + 'room_finish_id.csv', 'r'))
    for j in room_finish_reader:
        room_finish_id.append(j[0])

    # 错误列表
    room_error_id = []
    room_error_reader = csv.reader(open(pathname + 'room_error_id.csv', 'r'))
    for j in room_error_reader:
        room_error_id.append(j[0])

    # 待爬取列表
    room_id = []
    for j in room_all_id:
        if j not in room_finish_id:
            if j not in room_error_id:
                room_id.append(j[0])
    return room_id


def get_room(room_id):
    url = 'https://www.airbnb.com/api/v2/pdp_listing_details/' \
          '%s?' \
          '_format=for_rooms_show&' \
          'key=d306zoyjsyarp7ifhu67rjxn52tv0t20' % room_id

    # 如果网络未连接，等待Thread-1连接网络
    try:
        response = requests.get(url)
    except:
        sleep(15)
        response = requests.get(url)

    response.encoding = chardet.detect(response.content)['encoding']
    html = json.loads(response.text)

    # 房间id
    # print('房间id:%s' % room_id)

    # 房间图片src
    room_picture_src_img = []
    try:
        for j in range(5):
            room_picture_src_img.append(html['pdp_listing_detail']['photos'][j]['picture'])
        room_picture_src = []
        for j in room_picture_src_img:
            room_picture_src.append(str(j).split('?', 1)[0])
    except:
        try:
            for j in range(3):
                room_picture_src_img.append(html['pdp_listing_detail']['photos'][j]['picture'])
            room_picture_src = []
            for j in room_picture_src_img:
                room_picture_src.append(str(j).split('?', 1)[0])
        except:
            for j in range(1):
                room_picture_src_img.append(html['pdp_listing_detail']['photos'][j]['picture'])
            room_picture_src = []
            for j in room_picture_src_img:
                room_picture_src.append(str(j).split('?', 1)[0])
    # print('房间图片src:%s' % room_picture_src)

    # 房主id
    room_owner_id = html['pdp_listing_detail']['user']['id']
    # print('房主id:%s' % room_owner_id)

    # 房主头像src
    room_owner_img = html['pdp_listing_detail']['user']['profile_pic_path']
    room_owner_src = str(room_owner_img).split('?', 1)[0]
    # print('房主头像src:%s' % room_owner_src)

    # 评论页数
    # 评论总数
    count = html['pdp_listing_detail']['review_details_interface']['review_count']
    # 每页显示评论数
    per = html['pdp_listing_detail']['review_details_interface']['n_reviews_per_page']
    if count % per > 0:
        page = int(count / per) + 1
    else:
        page = int(count / per)

    return room_picture_src, room_owner_id, room_owner_src, page, per


def get_review(room_id, page, per):
    reviews_id = []
    reviews_rating = []
    reviewers_id = []
    reviewers_src = []
    for j in range(0, int(page)):
        reurl = 'https://www.airbnb.com/api/v2/homes_pdp_reviews?currency=CNY' \
                '&key=d306zoyjsyarp7ifhu67rjxn52tv0t20' \
                '&locale=en&' \
                'listing_id=%s' \
                '&_format=for_p3' \
                '&limit=7' \
                '&offset=%s' \
                '&order=language_country' % (str(room_id), str(j * per))
        response = requests.get(reurl)
        response.encoding = chardet.detect(response.content)['encoding']
        html = json.loads(response.text)

        # 评论信息
        reviews = html['reviews']
        for k in reviews:
            # 评论id
            reviews_id.append(k['id'])

            # 评论者id
            reviewers_id.append(k['reviewer']['id'])
            # 评论者src
            reviewers_src.append(str(k['reviewer']['picture_url']).split('?', 1)[0])
            # 评论者rating
            reviews_rating.append(k['rating'])
    # print('评论id(%s):%s' % (len(reviews_id), reviews_id))
    # print('评论rating(%s):%s' % (len(reviews_rating), reviews_rating))
    # print('评论者id(%s):%s' % (len(reviewers_id), reviewers_id))
    # print('评论者src(%s):%s' % (len(reviewers_src), reviewers_src))

    return reviews_id, reviews_rating, reviewers_id, reviewers_src


def write_table(pathname):

    # 判断是否已经写入表头
    try:
        with open(pathname + 'room.csv', 'r') as room_reader:
            if room_reader.readline() != '':
                return
            else:
                # 写入表头
                with open(pathname + 'room.csv', 'a') as room:
                    room_writer = csv.writer(room)

                    # 写入字段
                    fields = ['room_id', 'room_owner_id', 'picture_path', 'room_picture_src']
                    room_writer.writerow(fields)
                with open(pathname + 'user.csv', 'a') as user:
                    user_writer = csv.writer(user)

                    # 写入字段
                    fields = ['reviewers_id', 'picture_path', 'reviewers_src']
                    user_writer.writerow(fields)
                with open(pathname + 'room_user.csv', 'a') as room_user:
                    room_user_writer = csv.writer(room_user)

                    # 写入字段
                    fields = ['reviewers_id', 'reviews_id', 'room_id', 'reviews_rating']
                    room_user_writer.writerow(fields)
    except:
        # 写入表头
        with open(pathname + 'room.csv', 'a') as room:
            room_writer = csv.writer(room)

            # 写入字段
            fields = ['room_id', 'room_owner_id', 'picture_path', 'room_picture_src']
            room_writer.writerow(fields)
        with open(pathname + 'user.csv', 'a') as user:
            user_writer = csv.writer(user)

            # 写入字段
            fields = ['reviewers_id', 'picture_path', 'reviewers_src']
            user_writer.writerow(fields)
        with open(pathname + 'room_user.csv', 'a') as room_user:
            room_user_writer = csv.writer(room_user)

            # 写入字段
            fields = ['reviewers_id', 'reviews_id', 'room_id', 'reviews_rating']
            room_user_writer.writerow(fields)


def write_doc(pathname, room_id, room_owner_id, room_picture_src,
              reviewers_id, reviewers_src,
              reviews_id, reviews_rating,
              room_owner_src):
    # 房间信息room
    with open(pathname + 'room.csv', 'a') as room:
        room_writer = csv.writer(room)

        # 写入行数据
        for j in range(len(room_picture_src)):
            room_writer.writerow([room_id, room_owner_id,
                                  pathname+'room/'+'room_id_'+str(room_id)+'%'+str(j)+os.path.splitext(room_picture_src[j])[1],
                                  room_picture_src[j]])

    # 用户信息user
    with open(pathname + 'user.csv', 'a') as user:
        user_writer = csv.writer(user)

        # 写入行数据
        for j in range(len(reviewers_id)):
            user_writer.writerow([reviewers_id[j],
                                 pathname+'user/'+'user_id_'+str(reviewers_id[j])+os.path.splitext(reviewers_src[j])[1],
                                 reviewers_src[j]])

    # 房主信息owner
    with open(pathname + 'owner.csv', 'a') as owner:
        owner_writer = csv.writer(owner)

        # 写入行数据
        owner_writer.writerow([room_owner_id,
                               pathname+'owner/'+'owner_id_'+str(room_owner_id)+'%'+os.path.splitext(room_owner_src)[1],
                               room_owner_src])

    # 评论匹配room-user
    with open(pathname + 'room_user.csv', 'a') as room_user:
        room_user_writer = csv.writer(room_user)

        # 写入行数据
        for j in range(len(reviews_id)):
            room_user_writer.writerow([reviewers_id[j],
                                       reviews_id[j],
                                       room_id,
                                       reviews_rating[j]])

    # 已完成的room
    with open(pathname + 'room_finish_id.csv', 'a') as room_finish_id:
        room_finish_id_writer = csv.writer(room_finish_id)

        # 写入行数据
        room_finish_id_writer.writerow([room_id])


def write_error(pathname, room_id):
    with open(pathname + 'room_error_id.csv', 'a') as room_error_id:
        room_error_id_writer = csv.writer(room_error_id)

        # 写入行数据
        room_error_id_writer.writerow([room_id])


class NetWorkTread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        # 保证网络连接
        while True:
            get_network()


class MyThread(threading.Thread):
    def __init__(self, room_id, pathname):
        threading.Thread.__init__(self)
        self.room_id = room_id
        self.pathname = pathname

    def run(self):
        # 线程名
        thread_name = threading.current_thread().name

        finish = 0
        error = 0

        for j in self.room_id:
            time_start = time.time()

            print('--------------------------------------------------------------------')
            try:
                # 获取房间信息
                room_picture_src, room_owner_id, room_owner_src, page, per = get_room(j)

                # 获取评论信息
                reviews_id, reviews_rating, reviewers_id, reviewers_src = get_review(j, page, per)

                # 写入信息
                write_doc(self.pathname, j, room_owner_id, room_picture_src,
                          reviewers_id, reviewers_src,
                          reviews_id, reviews_rating,
                          room_owner_src)

                finish = finish + 1
                print('线程(%s):已完成%s个网页!' % (thread_name, finish))
            except Exception:
                os.system('spd-say "error"')
                print('\033[5;30;47m', end='')
                print('【错误：%s】' % j, end='')
                print('\033[0m', end='')
                print('获取数据出现异常！')
                # print(traceback.format_exc())

                # 写入信息
                write_error(my_pathname, j)

                error = error + 1
                print('线程(%s):已错误%s个网页!' % (thread_name, error))
                continue

            time_end = time.time()
            print('time:%s' % str(time_end-time_start))


if __name__ == '__main__':
    # 总开始时间
    start = time.time()

    # 本地下载路径
    my_pathname = r'../../data/'

    # 待爬取房间id
    my_room_id = list(set(get_room_id(my_pathname)))

    # 保证网络正常
    t = NetWorkTread()
    t.start()

    # 将房间id分为三等分
    my_room_id_1 = my_room_id[int(len(my_room_id) / 3) * 0: int(len(my_room_id) / 3) * 1]
    my_room_id_2 = my_room_id[int(len(my_room_id) / 3) * 1: int(len(my_room_id) / 3) * 2]
    my_room_id_3 = my_room_id[int(len(my_room_id) / 3) * 2: len(my_room_id)]

    # 创建csv,并赋值表头table
    write_table(my_pathname)

    # 执行多线程
    t1 = MyThread(room_id=my_room_id_1, pathname=my_pathname)
    t2 = MyThread(room_id=my_room_id_2, pathname=my_pathname)
    t3 = MyThread(room_id=my_room_id_3, pathname=my_pathname)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    # 总结束时间
    end = time.time()
    print('总用时:%s' % str(end - start))
