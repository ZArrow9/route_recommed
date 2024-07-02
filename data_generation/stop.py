import csv
import random
import math

# 生成100個隨機座標點
coordinates = []
for _ in range(100):
    x = random.randint(0, 250)
    y = random.randint(0, 250)
    coordinates.append((x, y))

# 創建100x100的矩陣並初始化為0
matrix = []
for _ in range(100):
    row = [0] * 100
    matrix.append(row)

# 根據座標計算時間（取整數）
for i in range(len(coordinates)):
    for j in range(len(coordinates)):
        if i != j:
            # 計算歐幾里得距離並取整數作為時間
            distance = math.sqrt((coordinates[i][0] - coordinates[j][0]) ** 2
                                 + (coordinates[i][1] - coordinates[j][1]) ** 2)
            matrix[i][j] = int(distance)
        else:
            # 自己到自己的時間為0
            matrix[i][j] = 0

# 將矩陣數據寫入 CSV 檔案
with open('stop.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for row in matrix:
        writer.writerow(row)
