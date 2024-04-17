from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://vuongmongo:dU8JZCbhGJ9M0un1@vuong-iot.ewsddrs.mongodb.net/admin2?retryWrites=true&w=majority&appName=Vuong-IoT"

# Tạo một client mới và kết nối tới server
client = MongoClient(uri)

# Lấy ra database "admin0"
db = client.admin2

collection = db.customer0

# Tài liệu bạn muốn chèn
document = {
    "name": "testDULIEU"
}
# Chèn tài liệu vào collection
try:
    collection.insert_one(document)
    document_count = collection.count_documents({})
    print("Đã chèn tài liệu thành công vào collection.")
    print("Số document hiện có là: ", document_count)
except Exception as e:
    print("Lỗi khi chèn tài liệu:", e)


 


