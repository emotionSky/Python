from pathlib import Path
import xlwings as xw  # pip install xlwings --user

src_folder = Path('./素材/月销售统计')
dst_folder = Path('./输出表格/月销售统计')
if not dst_folder.exists():
    dst_folder.mkdir(parents=True)

file_list = list(src_folder.glob('*.xlsx'))

# 参数 visible 用于设置 Excel 程序窗口的可见性
# 参数 add_book 用于设置启动 Excel 程序窗口后是否新建工作簿
app = xw.App(visible=False, add_book=False)

for i in file_list:
    if i.name.startswith('~$'):  # 跳过临时文件
        continue
    workbook = app.books.open(i)
    for j in workbook.sheets:
        data = j['A2'].expand('table').value  # 以 A2 为起点，从工作表中读取所有数据
        for index, val in enumerate(data):
            if val[2] == '背包':
                val[2] = '双肩包'
                data[index] = val
        j['A2'].expand('table').value = data

    dst_file = dst_folder / i.name
    workbook.save(str(dst_file))
    workbook.close()
app.quit()
