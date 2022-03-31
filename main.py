from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

def make_path(file_name: str):
    try:
        os.mkdir(f"paths/{file_name}")
    except: pass
    file = open(f"files/{file_name}", 'rb')
    i = 0
    while True:
        tmp = file.read(1048576)
        if len(tmp) == 0:
            break
        with open(f"paths/{file_name}/path_{i}", 'wb') as path_file:
            path_file.write(tmp)
        i += 1
        print(i * 1024)

#make_path("app.apk")

def make_one(file_name: str):
    file = open(f"new_{file_name}", 'wb')
    for f in os.listdir("paths/"):
        with open(f, 'rb') as path:
            tmp = path.read()
            file.write(tmp)

@app.get("/{file_name}")
async def get_data(file_name: str):
    return {"count": len(os.listdir(f"paths/{file_name}"))}

@app.get("/{file_name}/{path}", response_class=FileResponse)
async def upload_file(file_name: str, path: int):
    return FileResponse(f"paths/{file_name}/path_{path}")
