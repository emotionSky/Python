import win32com.client as win32  # pip install pywin32 --user
from pathlib import Path
import os

src_folder = Path('./素材')
dst_folder = Path('./标记关键词')
if not dst_folder.exists():
    dst_folder.mkdir()

src_file = src_folder / "员工考勤管理办法.docx"
dst_file = dst_folder / "处理后的员工考勤管理办法.docx"

word = win32.gencache.EnsureDispatch('Word.Application')
word.Visible = False
cs = win32.constants  # 导入Word开发接口提供的预设常量集合
doc = word.Documents.Open(os.path.abspath(src_file))
keyword_list = ['迟到', '早退', '旷工', '脱岗', '串岗']
color_list = [cs.wdRed, cs.wdGreen, cs.wdBlue, cs.wdYellow, cs.wdPink]

# 使用 zip() 函数将两个列表的关键词和颜色依次一一匹配
for w, c in zip(keyword_list, color_list):
    word.Options.DefaultHighlightColorIndex = c                # 设置突出显示的颜色
    findobj = word.Selection.Find                              # 创建一个 Find 对象，用于完成查找和替换
    findobj.ClearFormatting()                                  # 清除查找文本的格式设置，表示查找文本时不限制文本格式
    findobj.Text = w                                           # 设置查找的文本内容
    findobj.Replacement.ClearFormatting()                      # 清除替换文本的格式设置，为后续设置新的格式做好准备
    findobj.Replacement.Text = w                               # 将替换文本设置为查找文本相同的值
    findobj.Replacement.Font.Bold = True                       # 设置加粗
    findobj.Replacement.Font.Italic = True                     # 设置斜体
    findobj.Replacement.Font.Underline = cs.wdUnderlineDouble  # 设置双下划线
    findobj.Replacement.Highlight = True                       # 将文本做突出显示，使用前面设置突出显示的颜色
    # 执行查找和替换，参数 Replace 用于设置查找和替换的方式，此处 wdReplaceAll 表示一次性全部替换
    findobj.Execute(Replace=cs.wdReplaceAll)

doc.SaveAs(os.path.abspath(dst_file))
doc.Close()
word.Quit()
