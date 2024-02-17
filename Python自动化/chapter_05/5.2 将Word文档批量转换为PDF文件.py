from pathlib import Path
from comtypes.client import CreateObject  # pip install comtypes --user
import os

src_folder = Path('./合同文件')
des_folder = Path('./PDF文件')

# print(os.getcwd())  #查看当前工作目录
# print(os.path.abspath('.'))  #把相对路径转换为绝对路径
if not des_folder.exists():
    des_folder.mkdir(parents=True)

file_list = list(src_folder.glob('*.docx'))
# 使用 CreateObject 创建一个 Word 程序对象，可以理解为打开一个 Word 程序窗口
word = CreateObject('Word.Application')

for word_path in file_list:
    pdf_path = des_folder / word_path.with_suffix('.pdf').name
    if pdf_path.exists():
        continue
    else:
        doc = word.Documents.Open(os.path.abspath(word_path))
        # FileFormat 的 17 表示为pdf格式
        doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17)
        doc.Close()
word.Quit()
