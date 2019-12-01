# 从网站爬取相关信息，并下载数据到csv
# 获取房主头像
import requests
import chardet
import re
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


def get_owner_id(pathname):
    # 全列表
    room_all = []
    room_all_id = []
    room_all_id_reader = csv.reader(open(pathname + 'room2.csv', 'r'))
    for j in room_all_id_reader:
        room_all.append(j)
        room_all_id.append(j[0])

    # 已完成列表
    room_finish_id = []
    room_finish_reader = csv.reader(open(pathname + 'room_finish_id.csv', 'r'))
    for j in room_finish_reader:
        room_finish_id.append(j[0])
    room_finish_id_set = set(room_finish_id)

    # 错误列表
    room_error_id = []
    room_error_reader = csv.reader(open(pathname + 'room_error_id.csv', 'r'))
    for j in room_error_reader:
        room_error_id.append(j[0])
    room_error_id_set = set(room_error_id)

    # 待爬取列表
    room_id = []
    owner_id = []
    for j in range(1, len(room_all_id)):
        if room_all_id[j] not in room_finish_id_set:
            if room_all_id[j] not in room_error_id_set:
                room_id.append(room_all[j][0])
                owner_id.append(room_all[j][1])
    return room_id, owner_id


def get_owner(owner_id):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/78.0.3904.97 Safari/537.36'}

    url = 'https://www.airbnb.com/users/show/%s' % owner_id

    # 如果网络未连接，等待Thread-1连接网络
    try:
        response = requests.get(url, headers=headers)
    except:
        sleep(15)
        response = requests.get(url, headers=headers)

    response.encoding = chardet.detect(response.content)['encoding']
    html = response.text

    # 房主id
    print('房主id:%s' % owner_id)

    # 房主头像src
    reviewee = re.findall(r'"reviewee":{(.+?)}', html)[0]
    src = re.findall(r'"profile_pic_path":"(.+?)"', reviewee)[0]
    owner_src = str(src).split('?', 1)[0]
    print('房主头像src:%s' % owner_src)

    return owner_src


def write(pathname):
    # 写入表头
    with open(pathname + 'owner.csv', 'a') as owner:
        owner_writer = csv.writer(owner)

        # 写入字段
        fields = ['room_owner_id', 'picture_path', 'picture_src']
        owner_writer.writerow(fields)


def write_table(pathname):

    # 判断是否已经写入表头
    try:
        with open(pathname + 'owner.csv', 'r') as owner_reader:
            if owner_reader.readline() != '':
                return
            else:
                write(pathname)
    except:
        write(pathname)


def write_doc(pathname,
              owner_id, owner_src):
    # 房主信息owner
    with open(pathname + 'owner.csv', 'a') as owner:
        owner_writer = csv.writer(owner)

        # 写入行数据
        owner_writer.writerow([owner_id,
                              pathname+'owner/'+'owner_id_'+str(owner_id)+'%'+os.path.splitext(owner_src)[1],
                              owner_src])


def write_finish(pathname, room_id, owner_id):
    # 已完成的房主room_finish_id
    with open(pathname + 'owner_finish_id2.csv', 'a') as owner_finish_id:
        owner_finish_id_writer = csv.writer(owner_finish_id)

        # 写入行数据
        owner_finish_id_writer.writerow([owner_id])

    # 已完成的房间
    with open(pathname + 'room_finish_id.csv', 'a') as room_finish_id:
        room_finish_id_writer = csv.writer(room_finish_id)

        # 写入行数据
        room_finish_id_writer.writerow([room_id])


def write_error(pathname, room_id, owner_id):
    with open(pathname + 'owner_error_id2.csv', 'a') as owner_error_id:
        owner_error_id_writer = csv.writer(owner_error_id)

        # 写入行数据
        owner_error_id_writer.writerow([owner_id])

    # 已完成的房间
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
    def __init__(self, room_id, owner_id, pathname):
        threading.Thread.__init__(self)
        self.room_id = room_id
        self.owner_id = owner_id
        self.pathname = pathname

    def run(self):
        # 线程名
        thread_name = threading.current_thread().name

        finish = 0
        error = 0

        for j in range(len(self.owner_id)):
            time_start = time.time()

            print('--------------------------------------------------------------------')
            try:
                print('房间id:%s' % self.room_id[j])
                # 获取房主信息
                owner_src = get_owner(self.owner_id[j])

                # 写入信息
                write_doc(self.pathname,self.owner_id[j], owner_src)

                # 写入成功
                write_finish(self.pathname, self.room_id[j], self.owner_id[j])
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
                write_error(self.pathname, self.room_id[j], self.owner_id[j])

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

    # 待爬取房主id
    my_room_id, my_owner_id = get_owner_id(my_pathname)

    # 保证网络正常
    t = NetWorkTread()
    t.start()

    # 将房间id分为三等分
    my_room_id_1 = my_room_id[int(len(my_room_id) / 5) * 0: int(len(my_room_id) / 5) * 1]
    my_room_id_2 = my_room_id[int(len(my_room_id) / 5) * 1: int(len(my_room_id) / 5) * 2]
    my_room_id_3 = my_room_id[int(len(my_room_id) / 5) * 2: int(len(my_room_id) / 5) * 3]
    my_room_id_4 = my_room_id[int(len(my_room_id) / 5) * 3: int(len(my_room_id) / 5) * 4]
    my_room_id_5 = my_room_id[int(len(my_room_id) / 5) * 4: len(my_room_id)]

    # 将房主id分为三等分
    my_owner_id_1 = my_owner_id[int(len(my_owner_id) / 5) * 0: int(len(my_owner_id) / 5) * 1]
    my_owner_id_2 = my_owner_id[int(len(my_owner_id) / 5) * 1: int(len(my_owner_id) / 5) * 2]
    my_owner_id_3 = my_owner_id[int(len(my_owner_id) / 5) * 2: int(len(my_owner_id) / 5) * 3]
    my_owner_id_4 = my_owner_id[int(len(my_owner_id) / 5) * 3: int(len(my_owner_id) / 5) * 4]
    my_owner_id_5 = my_owner_id[int(len(my_owner_id) / 5) * 4: len(my_owner_id)]

    # 创建csv,并赋值表头table
    write_table(my_pathname)

    # 执行多线程
    t1 = MyThread(room_id=my_room_id_1, owner_id=my_owner_id_1, pathname=my_pathname)
    t2 = MyThread(room_id=my_room_id_2, owner_id=my_owner_id_2, pathname=my_pathname)
    t3 = MyThread(room_id=my_room_id_3, owner_id=my_owner_id_3, pathname=my_pathname)
    t4 = MyThread(room_id=my_room_id_4, owner_id=my_owner_id_4, pathname=my_pathname)
    t5 = MyThread(room_id=my_room_id_5, owner_id=my_owner_id_5, pathname=my_pathname)

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()

    # 总结束时间
    end = time.time()
    print('总用时:%s' % str(end - start))
