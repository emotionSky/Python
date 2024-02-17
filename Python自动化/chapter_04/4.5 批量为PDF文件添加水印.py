from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter  # pip install pypdf2 --user
from reportlab.lib.units import cm  # pip install reportlab --user
from reportlab.pdfgen import canvas
import reportlab.pdfbase.ttfonts


def create_watermark(content):
    file_name = '水印.pdf'
    # 设置水印文件的页面大小，默认的是 21cm x 29.7cm
    a = canvas.Canvas(file_name, pagesize=(30 * cm, 30 * cm))
    # 设置页面的坐标原点，默认是 (0,0)（左下角）
    a.translate(5 * cm, 0 * cm)
    # 注册水印的字体，非安装本机的字体
    reportlab.pdfbase.pdfmetrics.registerFont(
        reportlab.pdfbase.ttfonts.TTFont(
            '阿里巴巴普惠体', './fonts/Alibaba-PuHuiTi-Regular.ttf'))
    a.setFont('阿里巴巴普惠体', 25)
    a.rotate(30)                # 设置水印文字的旋转角度
    a.setFillColorRGB(0, 0, 0)  # 设置水印字体的填充颜色
    a.setFillAlpha(0.2)         # 设置水印字体的透明度

    # 绘制6行6列的水印文字
    for i in range(0, 30, 5):
        for j in range(0, 30, 5):
            # drawString() 的前两个参数是文字的坐标
            # 超出页面范围的水印显示不完整或不显示
            a.drawString(i * cm, j * cm, content)
    a.save()
    return file_name


def add_watermark(pdf_file_in, pdf_file_mark, pdf_file_out):
    outputfile = PdfWriter()
    inputfile = PdfReader(pdf_file_in)
    pageCount = len(inputfile.pages)
    markfile = PdfReader(pdf_file_mark)
    for i in range(pageCount):
        page = inputfile.pages[i]
        page.merge_page(markfile.pages[0]) # 添加水印
        outputfile.add_page(page)
    with open(pdf_file_out, 'wb') as f_out:
        outputfile.write(f_out)


src_folder = Path('./公告')
des_folder = Path('./水印公告')
if not des_folder.exists():
    des_folder.mkdir(parents=True)

file_list = list(src_folder.glob('*.pdf'))
for pdf in file_list:
    pdf_file_in = str(pdf)
    pdf_file_mark = create_watermark('巨潮资讯网')
    pdf_file_out = str(des_folder / pdf.name)
    add_watermark(pdf_file_in, pdf_file_mark, pdf_file_out)
