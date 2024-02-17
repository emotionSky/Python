from pathlib import Path
from PIL import Image

src_folder = Path('./要转换格式的图片')
des_folder = Path('./转换格式后的图片')

if not des_folder.exists():
    des_folder.mkdir(parents=True)
    
file_list = list(src_folder.glob('*.jpg'))
for i in file_list:
    des_file = des_folder / i.name
    des_file = des_file.with_suffix('.png')
    Image.open(i).save(des_file)
    print(f'{i.name} 完成格式转换！')
