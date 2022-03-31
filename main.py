from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os

app = FastAPI()


async def make_path(file: UploadFile) -> int:
    try:
        os.mkdir(f"paths/{file.filename}")
    except:
        pass
    i = 0
    while True:
        tmp = await file.read(1048576)
        if len(tmp) == 0:
            break
        with open(f"paths/{file.filename}/path_{i}", 'wb') as path_file:
            path_file.write(tmp)
        i += 1
    return i


def make_one(file_name: str):
    file = open(f"new_{file_name}", 'wb')
    for f in os.listdir("paths/"):
        with open(f, 'rb') as path:
            tmp = path.read()
            file.write(tmp)


@app.post("/upload")
async def upload_file(file: UploadFile):
    return {"count": await make_path(file)}


@app.get("/{file_name}")
async def get_data(file_name: str):
    return {"count": len(os.listdir(f"paths/{file_name}"))}


@app.get("/{file_name}/{path}", response_class=FileResponse)
async def download_file(file_name: str, path: int):
    return FileResponse(f"paths/{file_name}/path_{path}")
