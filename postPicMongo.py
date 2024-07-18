import base64
import json
from datetime import datetime

#Hàm kiểm tra xem mục đã tồn tại ở trong MongoDB hay chưa
def checkAvailable(db, ad_name, specific):
    try:
        #Đếm số lượng các mục chứa specific và trả về true nếu count > 0
        collection = db[ad_name]
        count = collection.count_documents({"specific": specific})
        return count > 0
    except Exception as e:
        return False

#hàm dùng đê lưu kết quả trích xuất xuống MongoDB
def mySave(db, image_data, ad_name, result_js, specific):
    try:
        #Kiểm tra xem specific đã được sử dụng hay chưa
        if (checkAvailable(db, ad_name, specific)):
            print("The specific has been used!!!")
            return False
        else:
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

#hàm dùng để lấy dữ liệu từ MongoDB
def myGet(db, ad_name, specific):
    #Kiểm tra xem mục đó đã được lưu hay chưa
    if (checkAvailable(db, ad_name, specific)):
        #Tạo ra một object để hứng kết quả trả về
        document = {
        }
        #Truy cập vào collection dựa trên ad_name
        collection = db[ad_name]
        #Tìm tài liệu dựa trên specific đã truyền vào
        pres_document = collection.find_one({"specific": specific}, {"_id" : False, "time" : False, "day" : False})
        document = pres_document
        return document
    else:
        print("----------")
        print("Not allow to get data of the document which is not exist!!")
        return False

#Hàm dùng để cập nhật dữ liệu ở trên MongoDB
def myUpdate(db, ad_name, specific, result_js, specificN):
    #Kiểm tra xem mục đó đã được lưu hay chưa
    if (checkAvailable(db, ad_name, specific)):
        #Tạo một object document để hứng dữ liệu mà sẽ được cập nhật và truy cập vào collection dựa trên ad_name
        document = {
            "presData" : {}
        }
        collection = db[ad_name]
        #Kiểm tra xem thông tin chỉnh sửa có bị trùng hay không
        if (specificN != specific and checkAvailable(db, ad_name, specificN)):
            print("The specific has been used!!!")
            return False
        else:
            #Cập nhật tên thuốc nếu có
            if result_js:
                #Load những dữ liệu từ result_js và đưa nó vào document để chuẩn bị cho việc cập nhật dữ liệu
                json_data = json.loads(result_js)
                document["presData"] = json_data
                #Cập nhật dữ liệu ở chỗ specific
                collection.update_one({"specific" : specific}, {"$set": document})
            #Cập nhật specific nếu có
            if specificN != specific:
                temp = {
                    "specific" : specificN
                }
                collection.update_one({"specific" : specific}, {"$set" : temp})
            print("Update Sucessfully!!")
            return True
    else:
        print("----------")
        print("Not allow to update the document which is not exist!!")
        return False
    
#hàm dùng để xóa dữ liệu đã lưu
def myDelete(db, ad_name, specific):
    #Kiểm tra xem mục đó đã được lưu hay chưa
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

#Hàm dùng để lấy thông tin lưu tổng quan
def myTotal(db, ad_name):
    #Truy cập vào MongoDB và đếm số lượng mục đã lưu
    collection = db[ad_name]
    count = collection.count_documents({})
    #Nếu mục đã lưu bằng 0 thì báo lỗi còn ngược lại sẽ in ra các thông tin cần thiết
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

