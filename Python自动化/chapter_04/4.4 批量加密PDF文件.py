from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter  # pip install pypdf2 --user

password = '123456'

src_folder = Path('./公告')
dst_folder = Path('./加密公告')
if not dst_folder.exists():
    dst_folder.mkdir(parents=True)

file_list = list(src_folder.glob('*.pdf'))
for pdf in file_list:
    inputfile = PdfReader(str(pdf))
    outputfile = PdfWriter()
    pageCount = len(inputfile.pages)
    for page in range(pageCount):
        outputfile.add_page(inputfile.pages[page])
    outputfile.encrypt(password)
    des_name = f'{pdf.stem}_secret.pdf'
    des_file = dst_folder / des_name
    with open(des_file, 'wb') as f_out:
        outputfile.write(f_out)
