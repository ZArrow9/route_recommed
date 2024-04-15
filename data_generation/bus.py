import csv
import random

# 創建空的矩陣
matrix = []

# 生成 100 列
for _ in range(100):
    # 隨機生成每列的公車數量（5 到 10 輛）
    bus_amount = random.randint(5, 10)
    # 創建一列，元素初始化為 0
    row = [0] * bus_amount
    
    # 生成不重複的隨機數填入列中
    for i in range(bus_amount):
        new_number = random.randint(1, 100)
        while new_number in row:
            new_number = random.randint(1, 100)
        row[i] = new_number
    
    # 將這一列加入矩陣中
    matrix.append(row)

# 將矩陣資料寫入 CSV 檔案
csv_file_path = 'bus.csv'
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for row in matrix:
        writer.writerow(row)


