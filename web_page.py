from fastapi import FastAPI, Request,Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from route import find_shortest_path
app = FastAPI()

# 创建 Jinja2Templates 实例并指定模板目录
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # 渲染 index.html 模板并返回
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit/")
async def submit_form(request: Request, start: int = Form(...), end: int = Form(...)):
    bus,shortest_path,time = find_shortest_path(start, end)
    return templates.TemplateResponse("result.html", {
        "request": request,
        "start":start,
        "end":end,
        "bus": bus,
        "shortest_path": shortest_path,
        "time": time
    })