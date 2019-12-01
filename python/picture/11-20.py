# 去除重复的owner和信息
# 将去重的.csv文件重新保存为2.csv文件
import csv
import time


# room_owner_id, picture_path, picture_src
def get_owner(pathname):
    owner_reader = csv.reader(open(pathname + 'owner.csv', 'r'))

    # 全部房主信息
    owner = []
    for j in owner_reader:
        owner.append(j)

    # 房主id
    room_owner_id = []
    room_owner_id_set = set(room_owner_id)
    # 本地路径
    picture_path = []
    # 服务器路径
    picture_src = []

    num = 0
    for j in range(1, len(owner)):
        if owner[j][0] not in room_owner_id_set:
            room_owner_id.append(owner[j][0])
            room_owner_id_set.add(owner[j][0])
            picture_path.append(owner[j][1])
            picture_src.append(owner[j][2])

            num = num + 1
            print(num)

    return room_owner_id, picture_path, picture_src


def table(pathname):
    # 写入表头
    with open(pathname + 'owner2.csv', 'w') as owner:
        owner_writer = csv.writer(owner)

        # 写入字段
        fields = ['room_owner_id', 'picture_path', 'picture_src']
        owner_writer.writerow(fields)


def write_table(pathname):
    # 判断是否已经写入表头
    try:
        with open(pathname + 'owner2.csv', 'r') as owner_reader:
            if owner_reader.readline() != '':
                return
            else:
                table(pathname)
    except:
        table(pathname)


def write_doc(pathname,
              room_owner_id, picture_path, picture_src,):

    # 用户信息user
    with open(pathname + 'owner2.csv', 'a') as owner:
        owner_writer = csv.writer(owner)

        # 写入行数据
        for j in range(len(room_owner_id)):
            owner_writer.writerow([room_owner_id[j],
                                  picture_path[j],
                                  picture_src[j]])


if __name__ == '__main__':
    start = time.time()

    my_pathname = '../../data/'
    # 写入表头
    write_table(my_pathname)

    # 获取用户信息
    my_room_owner_id, my_picture_path, my_picture_src = get_owner(my_pathname)

    write_doc(my_pathname,
              my_room_owner_id, my_picture_path, my_picture_src)

    end = time.time()
    print('time:%s' % str(end - start))
