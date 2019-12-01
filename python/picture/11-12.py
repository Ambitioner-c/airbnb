# 去除重复的room、user和room_user信息
# 将去重的.csv文件重新保存为2.csv文件
import csv
import os
import time


def write_table(pathname):

    # 判断是否已经写入表头
    try:
        with open(pathname + 'room2.csv', 'r') as room_reader:
            if room_reader.readline() != '':
                return
    except:
        # 写入表头
        with open(pathname + 'room2.csv', 'a') as room:
            room_writer = csv.writer(room)

            # 写入字段
            fields = ['room_id', 'room_owner_id', 'picture_path', 'room_picture_src']
            room_writer.writerow(fields)
        with open(pathname + 'user2.csv', 'a') as user:
            user_writer = csv.writer(user)

            # 写入字段
            fields = ['reviewers_id', 'picture_path', 'reviewers_src']
            user_writer.writerow(fields)
        with open(pathname + 'room_user2.csv', 'a') as room_user:
            room_user_writer = csv.writer(room_user)

            # 写入字段
            fields = ['reviewers_id', 'reviews_id', 'room_id', 'reviews_rating']
            room_user_writer.writerow(fields)


# 'room_id', 'room_owner_id', 'picture_path', 'room_picture_src'
def get_room(pathname):
    room_reader = csv.reader(open(pathname + 'room.csv', 'r'))

    # 全部房间信息
    room = []
    for j in room_reader:
        room.append(j)

    # 房间id
    room_id = []
    # 房主id
    room_owner_id = []
    # 本地路径
    picture_path = []
    # 服务器路径
    room_picture_src = []

    num = 0
    for j in range(1, len(room)-1):
        if room[j][2] not in picture_path:
            room_id.append(room[j][0])
            room_owner_id.append(room[j][1])
            picture_path.append(room[j][2])
            room_picture_src.append(room[j][3])

            num = num + 1
            print(num)

    return room_id, room_owner_id, picture_path, room_picture_src


# 'reviewers_id', 'picture_path', 'reviewers_src'
def get_user(pathname):
    user_reader = csv.reader(open(pathname + 'user.csv', 'r'))

    # 全部用户信息
    user = []
    for j in user_reader:
        user.append(j)

    # 评论者id
    reviewers_id = []
    # 本地路径
    picture_path = []
    # 服务器路径
    reviewers_src = []

    num = 0
    for j in range(1, len(user) - 1):
        if user[j][0] not in reviewers_id:
            reviewers_id.append(user[j][0])
            picture_path.append(user[j][1])
            reviewers_src.append(user[j][2])

            num = num + 1
            print(num)

    return reviewers_id, picture_path, reviewers_src


# 'reviewers_id', 'reviews_id', 'room_id', 'reviews_rating'
def get_room_user(pathname):
    room_user_reader = csv.reader(open(pathname + 'room_user.csv', 'r'))

    # 全部评论信息
    room_user = []
    for j in room_user_reader:
        room_user.append(j)

    # 评论者id
    reviewers_id = []
    # 评论id
    reviews_id = []
    # 房间id
    room_id = []
    # 评分
    reviews_rating = []

    num = 0
    for j in range(1, len(room_user) - 1):
        if room_user[j][1] not in reviews_id:
            reviewers_id.append(room_user[j][0])
            reviews_id.append(room_user[j][1])
            room_id.append(room_user[j][2])
            reviews_rating.append(room_user[j][3])

            num = num + 1
            print(num)

    return reviewers_id, reviews_id, room_id, reviews_rating


def write_doc(pathname,
              room_id, room_owner_id, picture_path, room_picture_src,
              reviewers_id, picture_path2, reviewers_src,
              reviewers_id3, reviews_id, room_id3, reviews_rating):
    # 房间信息room
    with open(pathname + 'room2.csv', 'a') as room:
        room_writer = csv.writer(room)

        # 写入行数据
        for j in range(len(room_picture_src)):
            room_writer.writerow([room_id[j],
                                  room_owner_id[j],
                                  picture_path[j],
                                  room_picture_src[j]])

    # 用户信息user
    with open(pathname + 'user2.csv', 'a') as user:
        user_writer = csv.writer(user)

        # 写入行数据
        for j in range(len(reviewers_id)):
            user_writer.writerow([reviewers_id[j],
                                  picture_path2[j],
                                 reviewers_src[j]])

    # 评论匹配room-user
    with open(pathname + 'room_user2.csv', 'a') as room_user:
        room_user_writer = csv.writer(room_user)

        # 写入行数据
        for j in range(len(reviews_id)):
            room_user_writer.writerow([reviewers_id3[j],
                                       reviews_id[j],
                                       room_id3[j],
                                       reviews_rating[j]])


if __name__ == '__main__':
    start = time.time()

    my_pathname = '../../data/'
    # 写入表头
    write_table(my_pathname)

    # 获取房间信息
    my_room_id, my_room_owner_id, my_picture_path, my_room_picture_src = get_room(my_pathname)

    # 获取用户信息
    my_reviewers_id, my_picture_path2, my_reviewers_src = get_user(my_pathname)

    # 获取评论信息
    my_reviewers_id3, my_reviews_id, my_room_id3, my_reviews_rating = get_room_user(my_pathname)

    write_doc(my_pathname,
              my_room_id, my_room_owner_id, my_picture_path, my_room_picture_src,
              my_reviewers_id, my_picture_path2, my_reviewers_src,
              my_reviewers_id3, my_reviews_id, my_room_id3, my_reviews_rating)

    end = time.time()
    print('time:%s' % str(end - start))
