from fastapi import FastAPI, File, UploadFile, Form, Response, Path
from pathlib import Path
from postPicMongo import mySave, myGet, myUpdate, myDelete, myTotal
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient


def init():
    uri = "mongodb+srv://vuongmongo:dU8JZCbhGJ9M0un1@vuong-iot.ewsddrs.mongodb.net/myApp?retryWrites=true&w=majority&appName=Vuong-IoT"
    client = MongoClient(uri)
    db = client['myApp']
    print('Successfull connect db')
    return db

app = FastAPI()
db = init()

@app.get("/get-result/")
async def get_result(ad_name: str = Path(), number: int = Path()):
    my_result = myGet(db, ad_name, number)
    if (my_result == False):
        return {"status": "fail"}
    else:
        print("-------------")
        print("Get successfully!!!")
        return my_result

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    # Xử lý lưu ảnh và cập nhật tên ảnh mới nhất
    main_image = file.file.read()
    # Code xử lý ảnh
    # --------------
    return {'presName1' : 'panadol', 'presName2' : 'libacid', 'presName3' : 'Kim tiền thảo'}

@app.post("/save-result/")
async def save_result(file: UploadFile = File(...), ad_name: str = Form(...), result_js: str = Form(...)):
    image = file.file.read()
    check = mySave(db, image, ad_name, result_js)
    if (check):
        return {"status" : "success"}
    else:
        return {"status" : "fail"}

@app.put("/update-result/")
async def update_result(ad_name: str = Form(...), number: int = Form(...), result_js: UploadFile = File(...)):
    check = myUpdate(db, ad_name, number, result_js)
    if (check):
        return {"status" : "success"}
    else:
        return {"status" : "fail"}

@app.delete("/delete-result/")
async def delete_result(ad_name: str = Path(), number: int = Path()):
    check = myDelete(db, ad_name, number)
    if (check):
        return {"status" : "success"}
    else:
        return {"status" : "fail"}

@app.get("/get-total/")
async def get_total(ad_name: str = Path()):
    my_result = myTotal(db, ad_name)
    if (my_result == False):
        return {"status": "fail"}
    else:
        print("-------------")
        print("Get total successfully!!!")
        return my_result




