import os
import shutil

src_folder = './要分类的文件'
des_folder = './分类后的文件'
files = os.listdir(src_folder)
print(files)
for file in files:
    src_path = src_folder + '/' + file
    if os.path.isfile(src_path):  # 只有文件才进行处理
        des_path = des_folder + '/' + file.split('.')[-1]
        if not os.path.exists(des_path):  # 文件夹不存在的时候需要先创建
            os.makedirs(des_path)
        # shutil.move(src_path, des_path)
        shutil.copy(src_path, des_path)
