import csv
import math

def load_data_from_csv():
    bus_data = []
    stop_data = []
    
    bus_file_path = './data_generation/bus.csv'
    stop_file_path = './data_generation/stop.csv'
    
    # 讀取 bus.csv 文件
    with open(bus_file_path, newline='') as bus_file:
        bus_reader = csv.reader(bus_file)
        for row in bus_reader:
            # 將每一行轉換為整數列表，並忽略空值
            temp_sublist = [int(value) for value in row if value.strip()]
            bus_data.append(temp_sublist)
    
    # 讀取 stop.csv 文件
    with open(stop_file_path, newline='') as stop_file:
        stop_reader = csv.reader(stop_file)
        for row in stop_reader:
            # 將每一行轉換為整數列表，如果值為空則設為 None
            int_row = [int(value) if value.strip() else None for value in row]
            stop_data.append(int_row)
    
    return bus_data, stop_data

# 廣度優先搜索（BFS）算法尋找可到達的路徑
def find_accessable_path(start:int, end, options: list[str]) -> list:
    
    time = 0
    # path 是一個列表，每個元素是 (bus, station, time)
    paths = [[(None, start, time)]]
    copy_path = []
    accessable_path = []
    data = []
    
    # 限制最多搜索 4 條路徑
    while len(copy_path) < 4:
        path = paths.pop(0)
        
        for bus, line in enumerate(bus_data):
            # 如果當前路徑的最後一站是目標站點，則跳出循環
            if path[-1][1] == end:
                break
            
            # 如果當前路徑的最後一站在這條公交線路上
            if path[-1][1] in line:
                for station in line:
                    copy_path = path.copy()

                    # 檢查該站點是否已經在路徑中，如果是則跳過
                    flag = False
                    for bus_, station_, time_ in copy_path:
                        if station == station_:
                            flag = True
                            break
                    if flag:    
                        continue
                    
                    # 計算從當前站點到新站點的時間
                    time = path[-1][2] + calculation(path[-1][1], station, bus)
                    copy_path.append((bus, station, time))
                    paths.append(copy_path)
                    
                    # 如果到達目標站點，則將該路徑加入可到達路徑列表中
                    if station == end:
                        accessable_path.append(copy_path)
                        
    # 根據選項對可到達路徑進行排序
    min_transfers = "min_transfers" in options
    shortest_time = "shortest_time" in options
    lowest_cost = "lowest_cost" in options
    
    if min_transfers:
        accessable_path.sort(key=len)
    
    if shortest_time:
        accessable_path = sorted(accessable_path, key=lambda x: x[-1][2])
    
    if lowest_cost:
        accessable_path = sorted(accessable_path, key=lambda x: x[-1][2])     
                      
    for i in accessable_path:
        data.append([(len(i) - 2), i[-1][2], math.ceil(i[-1][2] / 30)])    
    
    write_to_csv(accessable_path, 'data.csv')
        
    return data         

# 計算兩個站點之間的時間
def calculation(start, end, bus_line):
    route = []
    line = bus_data[bus_line]
    start_index = line.index(start)
    end_index = line.index(end)
    time = 0
    if start_index > end_index:
        route = line[end_index:start_index + 1]
        route.reverse()
    elif start_index < end_index:
        route = line[start_index:end_index + 1]
    time = cal_time(route)
    return time
          
# 計算路徑的總時間
def cal_time(short_path):
    total_time = 0
    for i in range(len(short_path) - 1):
        total_time = total_time + stop_data[short_path[i] - 1][short_path[i + 1] - 1]
    return total_time

# 處理最短路徑數據
def data_processing(shortest_path):
    bus = []
    new_shortest_path = []
    for data in range(len(shortest_path)):
        if data < len(shortest_path) - 1:
            line = shortest_path[data + 1][0]
            bus_route = bus_data[line]
            start_index = bus_route.index(shortest_path[data][1])
            end_index = bus_route.index(shortest_path[data + 1][1])
            if start_index > end_index:
                route = bus_route[end_index:start_index + 1]
                route.reverse()
            elif start_index < end_index:
                route = bus_route[start_index:end_index + 1]
           
            bus.append(line + 1)
            new_shortest_path.append(route)
            
    return bus, new_shortest_path, shortest_path[-1][2]

# 將可行路徑寫入 CSV 文件                       
def write_to_csv(accessable_path, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for path in accessable_path:
            writer.writerow(path)

# 載入數據
bus_data, stop_data = load_data_from_csv()
