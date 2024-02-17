from pathlib import Path
import xlwings as xw  # pip install xlwings --user

src_folder = Path('./素材/月销售统计')
dst_folder = Path('./输出表格/月销售统计')
if not dst_folder.exists():
    dst_folder.mkdir(parents=True)

file_list = list(src_folder.glob('*.xlsx'))
app = xw.App(visible=False, add_book=False)
sheet_name = '产品销售统计'
header = None
all_data = []

for i in file_list:
    if i.name.startswith('~$'):
        continue
    workbook = app.books.open(i)
    for j in workbook.sheets:
        if j.name == sheet_name:
            if header is None:
                header = j['A1:I1'].value
            data = j['A2'].expand('table').value
            all_data = all_data + data
    workbook.close()

new_workbook = xw.Book()
new_worksheet = new_workbook.sheets.add(sheet_name)
new_worksheet['A1'].value = header
new_worksheet['A2'].value = all_data
new_worksheet.autofit()  # 自动调整工作表的列宽和行高
new_workbook.save(dst_folder / '上半年产品销售统计表.xlsx')
new_workbook.close()

app.quit()
