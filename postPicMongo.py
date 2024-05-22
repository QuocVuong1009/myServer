import base64
import json

#Hàm để kiểm tra xem trong collection có dữ liệu hay không
def checkAvailable(db, ad_name, number):
    try:
        collection = db[ad_name]
        count = collection.count_documents({})
        return number > 0 and number <= count
    except Exception as e:
        return False

def mySave(db, image_data, ad_name, result_js):
    try:
        # Chuyển đổi dữ liệu hình ảnh sang base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        # Truy cập vào collection có tên là adname
        collection = db[ad_name]
        # Kiểm tra số lượng document đã có trong collection để thêm vào phần số thứ tự phân biệt
        count = collection.count_documents({}) + 1
        times = 'time' + str(count)
        # Tạo một document để lưu số thứ tự, hình ảnh thuốc và nội dung của đơn thuốc đó
        document = {
            "times" : times,
            "image" : image_base64,
            "presData" : {}
        }
        # Đọc nội dung của đơn thuốc là string result_js thành json để lưu nó vào MongoDB
        if result_js:
            json_data = json.loads(result_js)
            document["presData"] = json_data
        # Lưu
        collection.insert_one(document)
        print("----------")
        print("Save Successfully!")
        return True
    except Exception as e:
        print("----------")
        print("Error!!: ", e)
        return False

def myGet(db, ad_name, number):
    #Kiểm tra xem trong collection có dữ liệu đó hay chưa
    if (checkAvailable(db, ad_name, number)):
        #Tạo ra một object để hứng kết quả trả về
        document = {
        }
        #Truy cập vào collection và tạo biến times cho giống với quy ước đã lưu
        collection = db[ad_name]
        times = 'time' + str(number)
        #Tìm tài liệu dựa trên chỉ số thứ tự đã truyền vào
        pres_document = collection.find_one({"times": times}, {"_id" : False})
        document = pres_document
        return document
    else:
        print("----------")
        print("Not allow to get data of the document which is not exist!!")
        return False

def myUpdate(db, ad_name, number, result_js):
    #Kiểm tra xem trong collection có dữ liệu đó hay chưa
    if (checkAvailable(db, ad_name, number)):
        #tạo biến times để cho khớp với số thứ tự đã quy ước ở trong MongoDB
        times = "time" + str(number)
        #tạo một object document để hứng dữ liệu mà sẽ được cập nhật và truy cập vào collection dựa trên ad_name
        document = {
            "presData" : {}
        }
        collection = db[ad_name]
        if result_js:
            #Load những dữ liệu từ result_js và đưa nó vào document để chuẩn bị cho việc cập nhật dữ liệu
            resultJS_content = result_js.file.read()
            json_data = json.loads(resultJS_content)
            document["presData"] = json_data
            #Cập nhật dữ liệu ở chỗ có số thứ tự là times + number
            collection.update_one({"times" : times}, {"$set": document})
            print("Update Sucessfully!!")
            return True
        else:
            return False
    else:
        print("----------")
        print("Not allow to update the document which is not exist!!")
        return False
    
def myDelete(db, ad_name, number):
    #Kiểm tra xem trong document có dữ liệu đó hay chưa
    if (checkAvailable(db, ad_name, number)):
        #Tạo một document để hứng dữ liệu sẽ cập nhật sau khi xóa
        document = {
            "times"
        }
        #Kết nối vào collection và tạo các biến times và count để hỗ trợ việc cập nhật dữ liệu
        times = "time" + str(number)
        collection = db[ad_name]
        count = collection.count_documents({})
        #Xóa dữ liệu với chỉ số number
        collection.delete_one({"times" : times})
        #Cập nhật lại số thứ tự sau khi đã xóa
        for i in range (number + 1, count + 1):
            #Biến old dùng để lưu chỉ số cũ và biến new dùng để lưu chỉ số mới
            old = "time" + str(i)
            new = "time" + str(i-1)
            #Tìm kiếm chỉ số cũ và thay thế nó bằng chỉ số mới
            document = collection.find_one({"times": old})
            collection.update_one({"_id": document["_id"]}, {"$set": {"times": new}})
        print("Delete Sucessfully!!")
        return True
    else:
        print("----------")
        print("Not allow to delete the document which is not exist!!")
        return False


if __name__ == "__main__":
    with open("picture.jpg", "rb") as f:
        image_data = f.read()

