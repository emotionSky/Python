import win32com.client as win32  # pip install pywin32 --user
from pathlib import Path
import os


def ppt_conv(ppt_path, dst_folder):
    ppt_app = win32.gencache.EnsureDispatch('PowerPoint.Application')
    ppt = ppt_app.Presentations.Open(os.path.abspath(ppt_path))
    jpg_path = dst_folder / ppt_path.with_suffix('.jpg').name
    pdf_path = dst_folder / ppt_path.with_suffix('.pdf').name
    ppt.SaveAs(os.path.abspath(jpg_path), FileFormat=17)  # 这里的格式17是JPG
    ppt.SaveAs(os.path.abspath(pdf_path), FileFormat=32)  # 这里的格式32是PDF
    ppt.Close()
    ppt_app.Quit()


file_path = Path('./素材/PPT文件')
dst_folder = Path('./输出文件/导出PPT')
if not dst_folder.exists():
    dst_folder.mkdir()
file_list = file_path.glob('*.ppt*')
for i in file_list:
    if i.name.startswith("~$"):
        continue
    if i.is_file():
        ppt_conv(i, dst_folder)
