import os
import uvicorn
import aiofiles
from fastapi import FastAPI, HTTPException,  File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from typing import List

import service

uploadPath = "./data/latents/"


app = FastAPI()
# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 允许的前端地址
    allow_credentials=True,                  # 是否允许发送 Cookie
    allow_methods=["*"],                     # 允许的 HTTP 方法（GET、POST、PUT 等）
    allow_headers=["*"],                     # 允许的请求头
)

# 定义根路径的 GET 请求处理函数
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/dataList/{datatype}")
async def read_data(datatype):
    return service.getALlData()
        


    

# 定义带路径参数的 GET 请求处理函数
@app.get("/details/{name}")
async def read_item(name: str = None):
    data = service.getListByName("integration_accuracy.csv", name)
    return data

# 定义 POST 请求处理函数
@app.post("/upload")
async def upload_files(files:List[UploadFile] = File(...)):
    for file in files:
        save_path = os.path.join(uploadPath, file.filename)
        try:
            async with aiofiles.open(save_path, 'wb') as out_file:
                content = await file.read()
                await out_file.write(content)
        except Exception as e:
            return {"message": f"出现错误: {e}"}
        finally:
            # 关闭文件
            await file.close()
    return {"success":True, "message": f"文件 {file.filename} 已成功保存"}

if __name__ == "__main__":
    # 从环境变量中读取端口，默认为 8000
    port = int(os.getenv("APP_PORT", 8000))
    uvicorn.run(app, host="127.0.0.1", port=port)