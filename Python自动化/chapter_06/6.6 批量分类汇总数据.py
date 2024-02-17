import xlwings as xw  # pip install xlwings --user
import pandas as pd  # pip install pandas --user
from pathlib import Path

src_file = Path('./素材/产品销售统计表.xlsx')
dst_folder = Path('./输出表格')
if not dst_folder.exists():
    dst_folder.mkdir(parents=True)

app = xw.App(visible=False, add_book=False)
workbook = app.books.open(src_file)
worksheets = workbook.sheets
table = pd.DataFrame()

for i, j in enumerate(worksheets):
    # 读取工作表中的数据，并转换为 pandas 中的 DataFrame 格式
    data = j.range('A1').options(pd.DataFrame,
                                 header=1,
                                 index=False,
                                 expand='table').value
    # pandas  中的 reindex 函数可以改变行、列的顺序
    data = data.reindex(columns=[
        '单号', '销售日期', '产品名称', '成本价（元/个）', '销售价（元/个）', '销售数量（个）', '产品成本（元）',
        '销售收入（元）', '销售利润（元）'
    ])
    # 将改变列顺序后的数据追加
    table = table._append(data, ignore_index=True)

# workbook.close()

# 按照产品名称对数据进行分组
table = table.groupby('产品名称')
# 按照类别写入不同的工作表
# 新建一个工作簿
new_workbook = xw.books.add()
for idx, group in table:
    new_worksheet = new_workbook.sheets.add(idx)            # 添加工作表，并且以类别命名
    new_worksheet['A1'].options(index=False).value = group  # 数据
    # 选中工作表数据区域的右下角单元格
    last_cell = new_worksheet['A1'].expand('table').last_cell
    last_row = last_cell.row                    # 获取最后一行的行号
    last_column = last_cell.column              # 获取最后一列的列号
    last_column_letter = chr(64 + last_column)  # 在Excel中列是 ABCD……， 所以这里转换成字母
    sum_cell_name = f'{last_column_letter}{last_row + 1}'         # 得到最后求和结果的地址
    sum_last_row_name = f'{last_column_letter}{last_row}'         # 最后一个单元格的地址
    formula = f'=SUM({last_column_letter}2:{sum_last_row_name})'  # 调用 Excel 的求和公式
    new_worksheet[sum_cell_name].formula = formula
    new_worksheet.autofit()
    
new_workbook.save(dst_folder / '产品销售统计表（已汇总）.xlsx')
# new_workbook.close()
app.quit()
