from pathlib import Path
import win32com.client as win32  # pip install pywin32 --user
import os

src_folder = Path('./合同文件')
des_folder = Path('./替换关键词')
if not des_folder.exists():
    des_folder.mkdir(parents=True)

file_list = list(src_folder.glob('*.docx'))
replace_dict = {'中酿': '中亮', '订立': '签订'}
word = win32.gencache.EnsureDispatch('Word.Application')
word.Visible = False

cs = win32.constants  # 导入Word开发接口提供的预设常量集合
for file in file_list:
    doc = word.Documents.Open(os.path.abspath(file))
    print(file.name)
    for old_txt, new_txt in replace_dict.items():
        findobj = word.Selection.Find
        findobj.ClearFormatting()
        findobj.Text = old_txt
        findobj.Replacement.ClearFormatting()
        findobj.Replacement.Text = new_txt
        if findobj.Execute(Replace=cs.wdReplaceAll):
            print(f'{old_txt}-->{new_txt}')
    new_file = des_folder / file.name
    new_path = os.path.abspath(new_file)
    doc.SaveAs(os.path.abspath(new_file))
    doc.Close()
word.Quit()
