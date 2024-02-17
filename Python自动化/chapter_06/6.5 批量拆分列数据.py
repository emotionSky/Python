from pathlib import Path
import xlwings as xw  # pip install xlwings --user
import pandas as pd  # pip install pandas --user

src_folder = Path('./素材/每月进货统计表')
dst_folder = Path('./输出表格/拆分列')
if not dst_folder.exists():
    dst_folder.mkdir(parents=True)

file_list = list(src_folder.glob('*.xlsx'))
app = xw.App(visible=False, add_book=False)

for i in file_list:
    if i.name.startswith('~$'):
        continue
    workbook = app.books.open(i)
    worksheet = workbook.sheets['Sheet1']
    # 读取工作表中的数据，并转换为 pandas 中的 DataFrame 格式
    data = worksheet.range('A1').options(pd.DataFrame,
                                         header=1,
                                         index=False,
                                         expand='table').value
    # 将 产品尺寸（mm） 列中的数据以*分割
    new_data = data['产品尺寸（mm）'].str.split('*', expand=True)
    # 分割后得到的数据将要按照 长宽高 三个列来展示
    new_data.columns = ['长（mm）', '宽（mm）', '高（mm）']

    # 在 F 列后插入新列
    # new_data.shape[1] - 1 表示插入列的数量为拆分后列的数量-1
    for j in range(new_data.shape[1] - 1):
        worksheet['F:F'].insert(
            shift='right',                            # 插入新列后，原有的列向右移动
            copy_origin='format_from_left_or_above')  # 新列的格式从左侧的列复制

    # 将拆分的列写入工作表，F1 为写入的起始单元格
    worksheet['F1'].options(index=False).value = new_data
    worksheet.autofit()
    workbook.save(dst_folder / i.name)
    workbook.close()
app.quit()
