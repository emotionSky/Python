from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter  # pip install pypdf2 --user

src_folder = Path('./公告')
dst_folder = Path('./拆分公告')
if not dst_folder.exists():
    dst_folder.mkdir(parents=True)

file_list = list(src_folder.glob('*.pdf'))
step = 5
for pdf in file_list:
    inputfile = PdfReader(str(pdf))
    pages = len(inputfile.pages)

    # 小于 step 的不进行拆分
    if pages <= step:
        print(f'【{pdf.name}】页数为{pages}，小于等于每份页数{step}，不做拆分')
        continue

    # 超过 step 的进行拆分
    parts = pages // step + 1  # 整除运算符，丢掉小数部分
    for pt in range(parts):
        start = step * pt
        if pt != (parts - 1):
            end = start + step - 1
        else:  # 最后一份不一定是 step 的整数倍，所以需要特殊处理
            end = pages - 1
        outputfile = PdfWriter()
        for pn in range(start, end + 1):
            outputfile.add_page(inputfile.pages[pn])
        pt_name = f'{pdf.stem}_第{pt + 1}部分.pdf'
        pt_file = dst_folder / pt_name
        with open(pt_file, 'wb') as f_out:
            outputfile.write(f_out)
    print(f'【{pdf.name}】页数为{pages}，拆分为{parts}部分')
