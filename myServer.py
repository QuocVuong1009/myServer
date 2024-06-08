from fastapi import FastAPI, File, UploadFile, Form, Response, Path
from pathlib import Path
from postPicMongo import mySave, myGet, myUpdate, myDelete, myTotal
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
import extract
import preProcess
import cv2
import numpy as np 
import asyncio
from ultralytics import YOLO

model_detect = YOLO("./models/FULLDATA_V9.pt")
model_extract = YOLO("./models/recogonition_v8m.pt")

def init():
    uri = "mongodb+srv://vuongmongo:dU8JZCbhGJ9M0un1@vuong-iot.ewsddrs.mongodb.net/myApp?retryWrites=true&w=majority&appName=Vuong-IoT"
    client = MongoClient(uri)
    db = client['myApp']
    print('Successfull connect db')
    return db

def init_model():
    preProcess.init_preprocess("./models/yolov8_710.pt")
    extract.init_extract("./DrugDatabase/unique.csv")
    print("Sucessfull init model and connect csv")

app = FastAPI()
db = init()
init_model()

#OLD

# @app.get("/get-result/")
# async def get_result(ad_name: str = Path(), number: int = Path()):
#     my_result = myGet(db, ad_name, number)
#     if (my_result == False):
#         return {"status": "fail"}
#     else:
#         print("-------------")
#         print("Get successfully!!!")
#         return my_result

# @app.post("/upload-image/")
# async def upload_image(file: UploadFile = File(...), ad_name: str = Form(...)):
#     # Đọc bức ảnh và cập nhật tên file json
#     main_image = await file.read()
#     extract.update_json_file_path(ad_name) 
#     # Code xử lý ảnh
#     np_arr = np.fromstring(main_image, np.uint8)
#     image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
#     result = extract.extract_main(image)
#     # return result
#     if (result):
#         return result
#     else:
#         return {"status" : "fail"}

# @app.post("/save-result/")
# async def save_result(file: UploadFile = File(...), ad_name: str = Form(...), result_js: str = Form(...)):
#     image = file.file.read()
#     check = mySave(db, image, ad_name, result_js)
#     if (check):
#         return {"status" : "success"}
#     else:
#         return {"status" : "fail"}

# @app.put("/update-result/")
# async def update_result(ad_name: str = Form(...), number: int = Form(...), result_js: str = Form(...)):
#     check = myUpdate(db, ad_name, number, result_js)
#     if (check):
#         return {"status" : "success"}
#     else:
#         return {"status" : "fail"}

# @app.delete("/delete-result/")
# async def delete_result(ad_name: str = Path(), number: int = Path()):
#     check = myDelete(db, ad_name, number)
#     if (check):
#         return {"status" : "success"}
#     else:
#         return {"status" : "fail"}

# @app.get("/get-total/")
# async def get_total(ad_name: str = Path()):
#     my_result = myTotal(db, ad_name)
#     if (my_result == False):
#         return {"status": "fail"}
#     else:
#         print("-------------")
#         print("Get total successfully!!!")
#         return my_result

#CURRENT

# @app.get("/get-result/")
# async def get_result(ad_name: str = Path(), specific: str = Path()):
#     my_result = myGet(db, ad_name, specific)
#     if (my_result == False):
#         return {"status": "fail"}
#     else:
#         print("-------------")
#         print("Get successfully!!!")
#         return my_result

# async def process_image(main_image, ad_name):
#     extract.update_json_file_path(ad_name)
#     image_np = np.fromstring(main_image, np.uint8)
#     image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
#     result_json = await asyncio.to_thread(extract.extract_main, image, model_detect, model_extract)
#     return result_json

# @app.post("/upload-image/")
# async def upload_image(file: UploadFile = File(...), ad_name: str = Form(...)):
#     # Đọc bức ảnh và cập nhật tên file json
#     main_image = await file.read()
#     image_np = np.fromstring(main_image, np.uint8)
#     main_image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
#     extract.update_json_file_path(ad_name)
#     result_json = extract.extract_main(main_image, model_detect, model_extract)
#     if (result_json):
#         return result_json
#     else:
#         return {"status" : "fail"}

# @app.post("/save-result/")
# async def save_result(file: UploadFile = File(...), ad_name: str = Form(...), result_js: str = Form(...), specific: str = Form(...)):
#     image = file.file.read()
#     check = mySave(db, image, ad_name, result_js, specific)
#     if (check):
#         return {"status" : "success"}
#     else:
#         return {"status" : "fail"}

# @app.put("/update-result/")
# async def update_result(ad_name: str = Form(...), specific: str = Form(...), result_js: str = Form(...)):
#     check = myUpdate(db, ad_name, specific, result_js)
#     if (check):
#         return {"status" : "success"}
#     else:
#         return {"status" : "fail"}

# @app.delete("/delete-result/")
# async def delete_result(ad_name: str = Path(), specific: str = Path()):
#     check = myDelete(db, ad_name, specific)
#     if (check):
#         return {"status" : "success"}
#     else:
#         return {"status" : "fail"}

# @app.get("/get-total/")
# async def get_total(ad_name: str = Path()):
#     my_result = myTotal(db, ad_name)
#     if (my_result == False):
#         return {"status": "fail"}
#     else:
#         print("-------------")
#         print("Get total successfully!!!")
#         return my_result

#NEW

@app.get("/get-result/")
async def get_result(ad_name: str, specific: str):
    my_result = myGet(db, ad_name, specific)
    if not my_result:
        return {"status": "fail"}
    else:
        print("Get successfully!!!")
        return my_result

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...), ad_name: str = Form(...)):
    main_image = await file.read()
    image_np = np.frombuffer(main_image, np.uint8)
    main_image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    extract.update_json_file_path(ad_name)
    result_json = await asyncio.to_thread(extract.extract_main, main_image, model_detect, model_extract)
    if result_json:
        return result_json
    else:
        return {"status": "fail"}

@app.post("/save-result/")
async def save_result(file: UploadFile = File(...), ad_name: str = Form(...), result_js: str = Form(...), specific: str = Form(...)):
    image = await file.read()
    check = await asyncio.to_thread(mySave, db, image, ad_name, result_js, specific)
    if check:
        return {"status": "success"}
    else:
        return {"status": "fail"}

@app.put("/update-result/")
async def update_result(ad_name: str = Form(...), specific: str = Form(...), result_js: str = Form(...)):
    check = await asyncio.to_thread(myUpdate, db, ad_name, specific, result_js)
    if check:
        return {"status": "success"}
    else:
        return {"status": "fail"}

@app.delete("/delete-result/")
async def delete_result(ad_name: str, specific: str):
    check = await asyncio.to_thread(myDelete, db, ad_name, specific)
    if check:
        return {"status": "success"}
    else:
        return {"status": "fail"}

@app.get("/get-total/")
async def get_total(ad_name: str):
    my_result = myTotal(db, ad_name)
    if not my_result:
        return {"status": "fail"}
    else:
        print("Get total successfully!!!")
        return my_result
