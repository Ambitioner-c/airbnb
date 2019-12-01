# 获取本地存储room和user信息，并请求图片下载到本地
import csv
import requests
import traceback


# 'room_id', 'room_owner_id', 'picture_path', 'room_picture_src'
def get_room(pathname):
    room_reader = csv.reader(open(pathname+'room.csv', 'r'))

    # 全部房间信息
    room = []
    for j in room_reader:
        room.append(j)

    # 本地路径
    picture_path = []
    # 服务器路径
    room_picture_src = []

    for j in range(1, len(room)-1):
        picture_path.append(room[j][2])
        room_picture_src.append(room[j][3])

    # print(picture_path[0])
    # print(room_picture_src[0])

    return picture_path, room_picture_src


# 'reviewers_id', 'picture_path', 'reviewers_src'
def get_user(pathname):
    user_reader = csv.reader(open(pathname+'/user.csv', 'r'))

    # 全部用户信息
    user = []
    for j in user_reader:
        user.append(j)

    # 本地路径
    picture_path = []
    # 服务器路径
    reviewers_src = []

    for j in range(1, len(user)-1):
        picture_path.append(user[j][1])
        reviewers_src.append(user[j][2])

    # print(picture_path[0])
    # print(room_picture_src[0])

    return picture_path, reviewers_src


def download(picture_path, room_picture_src):
    try:
        pic = requests.get(room_picture_src)
    except Exception:
        print('【错误】当前图片无法下载!')
        print(traceback.format_exc())

        return
    try:
        with open(picture_path, 'wb') as wf:
            wf.write(pic.content)
    except Exception:
        print("【错误】写入失败!")
        print(traceback.format_exc())


if __name__ == '__main__':
    my_pathname = '../data/'
    # 获取房间的本地与服务器地址
    my_picture_path, my_room_picture_src = get_room(my_pathname)
    # 下载房间图片
    for i in range(len(my_picture_path)):
        download(my_picture_path[i], my_room_picture_src[i])

    # 获取用户的本地与服务器地址
    my_picture_path, my_reviewers_src = get_user(my_pathname)
    # 下载房间图片
    for i in range(len(my_picture_path)):
        download(my_picture_path[i], my_reviewers_src[i])
