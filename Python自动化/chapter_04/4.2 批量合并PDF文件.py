from pathlib import Path
from PyPDF2 import PdfReader, PdfMerger  # pip install pypdf2 --user

src_folder = Path('./公告')
des_file = Path('./合并公告/合并后的公告文件.PDF')
if not des_file.parent.exists():
    des_file.parent.mkdir(parents=True)
file_list = list(src_folder.glob('*.pdf'))
merger = PdfMerger()
outputPages = 0
for pdf in file_list:
    inputfile = PdfReader(str(pdf))
    merger.append(inputfile)
    pageCount = len(inputfile.pages)
    print(f'{pdf.name}  页数：{pageCount}')
    outputPages += pageCount
merger.write(str(des_file))
merger.close()
print(f'\n合并后的总页数：{outputPages}')
