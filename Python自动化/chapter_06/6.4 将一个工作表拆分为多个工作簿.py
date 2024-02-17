from pathlib import Path
import xlwings as xw  # pip install xlwings --user

src_file = Path('./素材/产品统计表.xlsx')
des_folder = Path('./输出表格/拆分统计表')
if not des_folder.exists():
    des_folder.mkdir(parents=True)

app = xw.App(visible=False, add_book=False)
workbook = app.books.open(src_file)
worksheet = workbook.sheets['统计表']
header = worksheet['A1:H1'].value
data1 = worksheet.range('A2').expand('table').value
data2 = dict()

for i in range(len(data1)):
    product_name = data1[i][1]
    if product_name not in data2:
        data2[product_name] = []
    data2[product_name].append(data1[i])
    
for k, v in data2.items():
    new_workbook = xw.books.add()
    new_worksheet = new_workbook.sheets.add(k)
    new_worksheet['A1'].value = header
    new_worksheet['A2'].value = v
    new_worksheet.autofit()
    new_workbook.save(des_folder / f'{k}.xlsx')
    new_workbook.close()
    
app.quit()
