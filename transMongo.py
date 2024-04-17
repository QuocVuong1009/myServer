# from pymongo.mongo_client import MongoClient
# uri = "mongodb+srv://vuongmongo:dU8JZCbhGJ9M0un1@vuong-iot.ewsddrs.mongodb.net/admin0?retryWrites=true&w=majority&appName=Vuong-IoT"
# # Create a new client and connect to the server
# client = MongoClient(uri)
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

from pymongo.mongo_client import MongoClient
from pymongo import UpdateOne
from PIL import Image
import io

uri = "mongodb+srv://vuongmongo:dU8JZCbhGJ9M0un1@vuong-iot.ewsddrs.mongodb.net/admin0?retryWrites=true&w=majority&appName=Vuong-IoT"

# Tạo một client mới và kết nối tới server
client = MongoClient(uri)

# Lấy ra database "admin0"
db = client.admin0

# Lấy ra collection mong muốn 
collection = db.customer1

# CHÈN TÀI LIỆU MỚI VÀ ĐẾM SỐ DOCUMENT ĐANG CÓ SẴN TRONG COLLECTION
# # Tài liệu bạn muốn chèn
# document = {
#     "name": "clnalvnl"
# }
# # Chèn tài liệu vào collection
# try:
#     collection.insert_one(document)
#     document_count = collection.count_documents({})
#     print("Đã chèn tài liệu thành công vào collection.")
#     print("Số document hiện có là: ", document_count)
# except Exception as e:
#     print("Lỗi khi chèn tài liệu:", e)

#CHÈN THÊM TÀI LIỆU VÀO COLLECTION MÀ TRONG ĐÓ CÓ MỘT DOCUMENT ĐÃ BIẾT
# Trường bạn muốn thêm vào tài liệu đã tồn tại
# update_document = {
#     "$set": {
#         "tien": "100ty"
#     }
# }
# # Tìm tài liệu có trường "name" là "vuong" và cập nhật nó để thêm trường "tien"
# try:
#     result = collection.update_one({"name": "vuong"}, update_document)
#     if result.modified_count > 0:
#         print("Đã chèn thành công trường 'tien' vào tài liệu.")
#     else:
#         print("Không tìm thấy tài liệu để chèn.")
# except Exception as e:
#     print("Lỗi khi chèn trường vào tài liệu:", e)

#IN RA CÁC THÔNG TIN VÀ CHỈ ĐỊNH ĐƯỢC IN VÀ KHÔNG IN CÁI NÀO
# Tìm kiếm các tài liệu trong collection có trường 'times' bằng '2'
# và chỉ bao gồm trường '_id' 'times' khi nó có giá trị False (tức là loại bỏ trường '_id' 'times' ra khỏi kết quả)
cursor = collection.find({"times": "2"}, {"_id": False, "times": False})
# Lặp qua các tài liệu tìm được và in ra thông tin
for document in cursor:
    print(document)

# IN RA THÔNG TIN DỮ LIỆU CỦA DOCUMENT Ở VỊ TRÍ CUỐI CÙNG
# Lấy document cuối cùng của collection
# last_document = collection.find_one({}, {"_id": False}, sort=[("_id", -1)])

# # In ra document cuối cùng
# print(last_document)

#CHÈN VÀO MỘT BỨC ẢNH
# Đọc nội dung của file hình ảnh
# with open("picture.jpg", "rb") as f:
#     image_data = f.read()

# update_document = {
#     "$set": {
#         "picture": image_data
#     }
# }
# # Tìm tài liệu có trường "name" là "vuong" và cập nhật nó để thêm trường "tien"
# try:
#     result = collection.update_one({"times": "2"}, update_document)
#     if result.modified_count > 0:
#         print("Đã chèn thành công ảnh vào tài liệu.")
#     else:
#         print("Không tìm thấy tài liệu để chèn.")
# except Exception as e:
#     print("Lỗi khi chèn trường vào tài liệu:", e)

# LOAD MỘT BỨC ẢNH NẾU BIẾT TRƯỚC MỘT TRƯỜNG.
# Tìm kiếm tài liệu có trường 'times' bằng '2' và lấy nội dung của trường 'image'
# document = collection.find_one({"times": "2"})
# image_data = document["picture"]

# # Đọc dữ liệu hình ảnh từ byte và hiển thị hình ảnh
# image = Image.open(io.BytesIO(image_data))
# image.show()


