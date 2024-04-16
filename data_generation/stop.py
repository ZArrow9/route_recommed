import csv
import random

matrix = []
for _ in range(100):
    row = [0] * 100
    matrix.append(row)

# 設定 b1 和 b2 之間的距離
matrix[0][1] = 1

# 填充矩陣中的時間值
for row in range(len(matrix)):
    for col in range(len(matrix)):
        if (row == 0) and (col > 1):
            # 從 b1 到其他站點的時間
            matrix[row][col] = matrix[row][col - 1] + random.randint(1, 3)
        elif row != 0:
            if row > col:
                # 使用對稱性填充現有值
                matrix[row][col] = matrix[col][row]
            elif row < col:
                # 基於前一列計算時間
                matrix[row][col] = (matrix[row - 1][col] - matrix[row - 1][row])

# 將矩陣數據寫入 CSV 檔案
with open('stop.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for row in matrix:
        writer.writerow(row)
