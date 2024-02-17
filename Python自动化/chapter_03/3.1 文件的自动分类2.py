from pathlib import Path

src_folder = Path('./要分类的文件')
des_folder = Path('./分类后的文件')

files = src_folder.glob('*')
for file in files:
    if file.is_file():  # 确保文件才能操作
        # suffix 可以提取文件扩展名, / 是pathlib模块特有的路径拼接运算符
        des_path = des_folder / file.suffix.strip('.')
        if not des_path.exists():
            des_path.mkdir(parents=True)  # parents=True 自动创建多级文件夹
        file.replace(des_path / file.name)  # replace 将文件移动
        
""" pathlib的操作可以参考 https://blog.csdn.net/qq_27071221/article/details/130657733 """
