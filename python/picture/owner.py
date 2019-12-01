# 获取本地存储owner信息，并请求图片下载到本地（11-12）
# 添加了已完成、错误文件（11-12）
# 联网功能（11-12）
# 多线程（11-12）
import csv
import requests
import threading
import subprocess
from subprocess import run
import os
import time
from time import sleep


def get_network(username, password):
    ip = 'www.baidu.com'

    # 执行命令行指令并返回结果
    before = run('ping -c 1 %s' % ip, shell=True, stdout=subprocess.PIPE)

    # 如果返回值是0表示连通，否则为断开
    before_code = before.returncode
    if before_code == 0:

        return
    else:
        data = {'DDDDD': username, 'upass': password, '0MKKey': '123'}
        requests.post('http://172.16.200.13', data=data)
        print('线程-1联网！')

        return


# 'room_owner_id', 'picture_path', 'picture_src'
def get_owner(pathname):
    # 开始时间
    start = time.time()

    # 全部用户
    owner_all = []
    owner_all_reader = csv.reader(open(pathname+'owner2.csv', 'r'))
    for j in owner_all_reader:
        owner_all.append(j)

    # 已完成用户
    owner_finish_id = []
    owner_finish_id_reader = csv.reader(open(pathname + 'owner_finish_id.csv', 'r'))
    for j in owner_finish_id_reader:
        owner_finish_id.append(j[0])
    owner_finish_id_set = set(owner_finish_id)

    # 错误用户
    owner_error_id = []
    owner_error_id_reader = csv.reader(open(pathname + 'owner_error_id.csv', 'r'))
    for j in owner_error_id_reader:
        owner_error_id.append(j[0])
    owner_error_id_set = set(owner_error_id)

    # 房主id
    room_owner_id = []
    # 本地路径
    picture_path = []
    # 服务器路径
    picture_src = []

    # 待爬取图片
    for j in range(1, len(owner_all)-1):
        if owner_all[j][0] not in owner_finish_id_set:
            if owner_all[j][0] not in owner_error_id_set:
                room_owner_id.append(owner_all[j][0])
                picture_path.append(owner_all[j][1])
                picture_src.append(owner_all[j][2])

    # 结束时间
    end = time.time()
    print('获取带爬取图片总用时：%s' % str(end - start))
    return room_owner_id, picture_path, picture_src


def write_doc(pathname, room_owner_id):
    # 用户path
    with open(pathname + 'owner_finish_id.csv', 'a') as owner_finish_id:
        owner_finish_id_writer = csv.writer(owner_finish_id)

        # 写入行数据
        owner_finish_id_writer.writerow([room_owner_id])


def write_error(pathname, room_owner_id):
    with open(pathname + 'owner_error_id.csv', 'a') as owner_error_id:
        owner_error_id_writer = csv.writer(owner_error_id)

        # 写入行数据
        owner_error_id_writer.writerow([room_owner_id])


class NetWorkTread(threading.Thread):
    def __init__(self, username, password):
        threading.Thread.__init__(self)
        self.username = username
        self.password = password

    def run(self):
        # 保证网络连接
        while True:
            get_network(self.username, self.password)


class MyThread(threading.Thread):
    def __init__(self, pathname, room_owner_id, picture_path, picture_src):
        threading.Thread.__init__(self)
        self.pathname = pathname
        self.room_owner_id = room_owner_id
        self.picture_path = picture_path
        self.picture_src = picture_src

    def run(self):
        # 线程名
        thread_name = threading.current_thread().name

        finish = 0
        error = 0

        for j in range(len(self.room_owner_id)):
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                     'Chrome/78.0.3904.97 Safari/537.36'}
            # 开始时间
            start = time.time()

            print('******************************')
            try:
                res = requests.get(self.picture_src[j], headers=headers)
            except:
                sleep(15)
                res = requests.get(self.picture_src[j], headers=headers)

            if res.status_code == '404':

                # 写入错误
                write_error(self.pathname, self.room_owner_id[j])

                error = error + 1
                os.system('spd-say "error"')
                print('\033[5;30;47m', end='')
                print('线程(%s):已错误%s张图片!' % (thread_name, error))
                print('\033[0m')

                continue
            else:
                with open(self.picture_path[j], 'wb') as wf:
                    # 下载图片
                    wf.write(res.content)

                    # 写入成功
                    write_doc(self.pathname, self.room_owner_id[j])

                    finish = finish + 1
                    print('线程(%s):已完成%s张图片!' % (thread_name, finish))

            # 结束时间
            end = time.time()
            print('time:%s' % str(end - start))


if __name__ == '__main__':
    # 本地下载路径
    my_pathname = '../../data/'

    # 校园网账号
    my_username = '2016214436'
    # 校园网密码
    my_password = '656359504'
    # 保证网络正常
    t = NetWorkTread(my_username, my_password)
    t.start()

    # 获取房间的本地与服务器地址
    my_room_owner_id, my_picture_path, my_picture_src = get_owner(my_pathname)

    # 将id分为三等分
    my_room_owner_id_1 = my_room_owner_id[int(len(my_room_owner_id) / 5) * 0: int(len(my_room_owner_id) / 5) * 1]
    my_room_owner_id_2 = my_room_owner_id[int(len(my_room_owner_id) / 5) * 1: int(len(my_room_owner_id) / 5) * 2]
    my_room_owner_id_3 = my_room_owner_id[int(len(my_room_owner_id) / 5) * 2: int(len(my_room_owner_id) / 5) * 3]
    my_room_owner_id_4 = my_room_owner_id[int(len(my_room_owner_id) / 5) * 3: int(len(my_room_owner_id) / 5) * 4]
    my_room_owner_id_5 = my_room_owner_id[int(len(my_room_owner_id) / 5) * 4: len(my_room_owner_id)]

    # 将房间path分为三等分
    my_picture_path_1 = my_picture_path[int(len(my_picture_path) / 5) * 0: int(len(my_picture_path) / 5) * 1]
    my_picture_path_2 = my_picture_path[int(len(my_picture_path) / 5) * 1: int(len(my_picture_path) / 5) * 2]
    my_picture_path_3 = my_picture_path[int(len(my_picture_path) / 5) * 2: int(len(my_picture_path) / 5) * 3]
    my_picture_path_4 = my_picture_path[int(len(my_picture_path) / 5) * 3: int(len(my_picture_path) / 5) * 4]
    my_picture_path_5 = my_picture_path[int(len(my_picture_path) / 5) * 4: len(my_picture_path)]

    # 将房间src分为三等分
    my_picture_src_1 = my_picture_src[int(len(my_picture_src) / 5) * 0: int(len(my_picture_src) / 5) * 1]
    my_picture_src_2 = my_picture_src[int(len(my_picture_src) / 5) * 1: int(len(my_picture_src) / 5) * 2]
    my_picture_src_3 = my_picture_src[int(len(my_picture_src) / 5) * 2: int(len(my_picture_src) / 5) * 3]
    my_picture_src_4 = my_picture_src[int(len(my_picture_src) / 5) * 3: int(len(my_picture_src) / 5) * 4]
    my_picture_src_5 = my_picture_src[int(len(my_picture_src) / 5) * 4: len(my_picture_src)]

    # 执行多线程
    t1 = MyThread(pathname=my_pathname, room_owner_id=my_room_owner_id_1, picture_path=my_picture_path_1, picture_src=my_picture_src_1)
    t2 = MyThread(pathname=my_pathname, room_owner_id=my_room_owner_id_2, picture_path=my_picture_path_2, picture_src=my_picture_src_2)
    t3 = MyThread(pathname=my_pathname, room_owner_id=my_room_owner_id_3, picture_path=my_picture_path_3, picture_src=my_picture_src_3)
    t4 = MyThread(pathname=my_pathname, room_owner_id=my_room_owner_id_4, picture_path=my_picture_path_4, picture_src=my_picture_src_4)
    t5 = MyThread(pathname=my_pathname, room_owner_id=my_room_owner_id_5, picture_path=my_picture_path_5, picture_src=my_picture_src_5)

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
