import base64
import json
from datetime import datetime

def checkAvailable(db, ad_name, specific):
    try:
        collection = db[ad_name]
        count = collection.count_documents({"specific": specific})
        return count > 0
    except Exception as e:
        return False

def mySave(db, image_data, ad_name, result_js, specific):
    try:
        # Chuyển đổi dữ liệu hình ảnh sang base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        # Truy cập vào collection có tên là ad_name
        collection = db[ad_name]
        # Lấy thời gian hiện tại
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_day = now.strftime("%Y-%m-%d")
        # Tạo một document để lưu số thứ tự, hình ảnh thuốc và nội dung của đơn thuốc đó
        document = {
            "specific": specific,
            "image": image_base64,
            "time": current_time,
            "day": current_day,
            "presData": {}
            
        }
        # Chuyển đổi string JSON nội dung đơn thuốc thành dictionary và lưu nó vào MongoDB
        if result_js:
            json_data = json.loads(result_js)
            document["presData"] = json_data
        # Lưu document vào collection
        collection.insert_one(document)
        print("----------")
        print("Save Successfully!")
        return True
    except Exception as e:
        print("----------")
        print("Error!!: ", e)
        return False

def myGet(db, ad_name, specific):
    #Kiểm tra xem trong collection có dữ liệu đó hay chưa
    if (checkAvailable(db, ad_name, specific)):
        #Tạo ra một object để hứng kết quả trả về
        document = {
        }
        #Truy cập vào collection dựa trên ad_name
        collection = db[ad_name]
        #Tìm tài liệu dựa trên chỉ số thứ tự đã truyền vào
        pres_document = collection.find_one({"specific": specific}, {"_id" : False, "time" : False, "day" : False})
        document = pres_document
        return document
    else:
        print("----------")
        print("Not allow to get data of the document which is not exist!!")
        return False

def myUpdate(db, ad_name, specific, result_js, specificN):
    #Kiểm tra xem trong collection có dữ liệu đó hay chưa
    if (checkAvailable(db, ad_name, specific)):
        #tạo một object document để hứng dữ liệu mà sẽ được cập nhật và truy cập vào collection dựa trên ad_name
        document = {
            "presData" : {}
        }
        collection = db[ad_name]
        if result_js:
            #Load những dữ liệu từ result_js và đưa nó vào document để chuẩn bị cho việc cập nhật dữ liệu
            # resultJS_content = result_js.file.read()
            json_data = json.loads(result_js)
            document["presData"] = json_data
            #Cập nhật dữ liệu ở chỗ có số thứ tự là number
            collection.update_one({"specific" : specific}, {"$set": document})
            if specificN:
                temp = {
                    "specific" : specificN
                }
                collection.update_one({"specific" : specific}, {"$set" : temp})
            print("Update Sucessfully!!")
            return True
        else:
            return False
    else:
        print("----------")
        print("Not allow to update the document which is not exist!!")
        return False
    
def myDelete(db, ad_name, specific):
    #Kiểm tra xem trong document có dữ liệu đó hay chưa
    if (checkAvailable(db, ad_name, specific)):
        #Kết nối vào collection dựa vào ad_name
        collection = db[ad_name]
        #Xóa dữ liệu với specific
        collection.delete_one({"specific" : specific})
        print("Delete Sucessfully!!")
        return True
    else:
        print("----------")
        print("Not allow to delete the document which is not exist!!")
        return False

def myTotal(db, ad_name):
    collection = db[ad_name]
    count = collection.count_documents({})
    if count == 0:
        print("----------")
        print("Not allow to get the data of the document which is not exist!!")
        return False
    else:
        documents = list(collection.find({}, {"_id": 0, "specific": 1, "time": 1, "day": 1}).sort([("day", -1), ("time", -1)]))  
        return documents

if __name__ == "__main__":
    with open("picture.jpg", "rb") as f:
        image_data = f.read()

