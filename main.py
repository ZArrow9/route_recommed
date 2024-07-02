import csv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import route 
import ast

app = FastAPI()

# 建立 Jinja2Templates 實例並指定模板目錄
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # 渲染 index.html 模板並返回
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit/")
async def submit_form(request: Request,
                      start: int = Form(...),
                      end: int = Form(...),
                      options: list[str] = Form(None)):
    # 從 route 模組中尋找最短路徑
    data= route.find_accessable_path(start, end, options)
    
    # 返回結果的 HTML 模板頁面
    return templates.TemplateResponse("submit.html", {
        "request": request,
        "start": start,
        "end": end,
        "options":options,
        "data":data
    })
    
@app.post("/result/")
async def submit_form(request: Request,
                      index:int=Form(...)):
    bus_data=[]
    data_path = 'data.csv'
    with open(data_path, newline='') as data_file:
        data_reader = csv.reader(data_file)
        for i in data_reader:
            tuple_list = [ast.literal_eval(item) for item in i]
            bus_data.append(tuple_list)    
            
    bus,shortest_path,time = route.data_processing(bus_data[index])
    
    # 返回結果的 HTML 模板頁面
    return templates.TemplateResponse("result.html", {
        "request": request,
        "bus": bus,
        "shortest_path": shortest_path,
        "time": time
    })
