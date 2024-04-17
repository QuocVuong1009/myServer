from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from tempfile import NamedTemporaryFile
from pathlib import Path
from magic import Magic
from postPicMongo import myPOST, myGET

magic = Magic()
app = FastAPI()
upload_folder = "uploaded_images"
Path(upload_folder).mkdir(parents=True, exist_ok=True)


@app.post("/upload-image/")
async def upload_image(file: UploadFile, urlDatabase: str, adName: str):
    # Xử lý lưu ảnh và cập nhật tên ảnh mới nhất
    main_image = file.file.read()
    #Code xử lý ảnh
    #--------------
    myPOST(main_image, urlDatabase, adName)


@app.get("/get-image/")
async def get_image(urlDatabase: str, adName: str):
    myImage = myGET(urlDatabase, adName)
    if (myImage == False):
        raise HTTPException(status_code=404, detail="There are no picture in this field")
    else:
        with NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(myImage)
                temp_file_path = temp_file.name    
        # Trả về hình ảnh từ tệp tạm thời
        return FileResponse(temp_file_path, media_type="image/jpeg")
