from pathlib import Path

while True:
    folder = input('请输入要在哪个文件夹（如【D:\\】或【D:\\案例\\】）下进行查找：')
    folder = Path(folder.strip())
    if folder.exists() and folder.is_dir():
        break
    else:
        print('输入的路径不存在或不正确，请重新输入！')
        
keyword = input('请输入要查找的文件或文件夹的名称：').strip()
result = list(folder.rglob(keyword)) # rglob 会以folder为起点，层级向下查找

if len(result) != 0:
    print(f'在【{folder}】下查找到以下名为【{keyword}】的文件或文件夹：')
    for i in result:
        print(i)
else:
    print(f'在【{folder}】下未查找到名为【{keyword}】的文件或文件夹！')
