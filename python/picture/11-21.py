# 替换文件名中的%
import os

old_files = os.listdir('owner')

new_files = []
for i in old_files:
    new_files.append(i.replace('%', ''))

for i in range(len(old_files)):
    print('************************')
    old_file = old_files[i]
    old_file = '../../data/owner/' + old_file
    
    new_file = new_files[i]
    new_file = '../../data/owner/' + new_file
    
    print(old_file)
    print(new_file)

    os.rename(old_file, new_file)
