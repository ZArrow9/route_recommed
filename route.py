import csv

def load_data_from_csv():
    bus_data = []
    stop_data = []
    
    bus_file_path = r'C:\Users\user\Desktop\專題\data_generation\bus.csv'
    stop_file_path = r'C:\Users\user\Desktop\專題\data_generation\stop.csv'
    # 讀取 bus.csv 檔案
    with open(bus_file_path, newline='') as bus_file:
        bus_reader = csv.reader(bus_file)
        for row in bus_reader:
            # 將每個值轉換為整數，並過濾空值
            temp_sublist = [int(value) for value in row if value.strip()]
            bus_data.append(temp_sublist)
    
    # 讀取 stop.csv 檔案
    with open(stop_file_path, newline='') as stop_file:
        stop_reader = csv.reader(stop_file)
        for row in stop_reader:
            # 將每個值轉換為整數
            int_row = [int(value) if value.strip() else None for value in row]
            stop_data.append(int_row)
    
    return bus_data, stop_data
# bfs
def find_shortest_path(start:int, end) -> list:
    if start < 1 or start > 100 or end < 1 or end > 100:
        return []
    
    if start == end:
        return []
    time=0
    # path is a list of (bus, station, time)
    paths = [[(None, start, time)]] 
    copy_path=[]
    accessable_path=[]
    shortest_path=[]
    #開始搜尋
    while len(copy_path)<4:
        
        path = paths.pop(0)
        
        for bus, line in enumerate(bus_data):
            #如果該路線已抵達終點，該路線就不用再搜尋
            if path[-1][1]==end:
                break
            #開始搜尋
            if path[-1][1] in line:
                for station in line:
                    copy_path = path.copy()

                    # 判斷是否經過過
                    flag = False
                    for bus_, station_ ,time_ in copy_path:
                        if station == station_:
                            flag = True
                            break
                    if flag:    
                        continue
                    
                    time=path[-1][2]+calculation(path[-1][1],station,bus)
                    copy_path.append((bus, station, time))
                    paths.append(copy_path)
                    
                    if station == end:
                        accessable_path.append(copy_path)
    
    
    #選出所花時間最短路線
    short_time = float('inf')    
    for p in accessable_path:
        time_p = p[-1][2]
        if time_p < short_time:
            shortest_path = [p]
            short_time = time_p
        elif time_p == short_time:
            shortest_path.append(p)
    bus_number,new_shortpath=data_processing(shortest_path[-1])
    return bus_number,new_shortpath,shortest_path[-1][-1][2]
                               
        
def calculation(start,end,bus_line):
    route=[]
    line=bus_data[bus_line]
    start_index=line.index(start)
    end_index=line.index(end)
    time=0
    if start_index>end_index:
        route=line[end_index:start_index+1]
        route.reverse()
    elif start_index<end_index:
        route=line[start_index:end_index+1]
    time=cal_time(route)
    return time
          
def cal_time(short_path):
    total_time=0
    for i in range(len(short_path)-1):
        total_time=total_time+stop_data[short_path[i]-1][short_path[i+1]-1]
    return total_time

def data_processing(shortest_path):
    bus=[]
    new_shortest_path=[]
    for data in range(len(shortest_path)):
        if data<len(shortest_path)-1:
            line=shortest_path[data+1][0]
            bus_route=bus_data[line]
            start_index=bus_route.index(shortest_path[data][1])
            end_index=bus_route.index(shortest_path[data+1][1])
            if start_index>end_index:
                route=bus_route[end_index:start_index+1]
                route.reverse()
            elif start_index<end_index:
                route=bus_route[start_index:end_index+1]
           
            bus.append(line+1)
            new_shortest_path.append(route)
            
    return bus,new_shortest_path

bus_data, stop_data = load_data_from_csv()
