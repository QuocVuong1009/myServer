from pymongo.mongo_client import MongoClient

def checkAvailable(uri, database_name, collection_name):
    try:
        client = MongoClient(uri)
        db = client[database_name]
        collection = db[collection_name]
        count = collection.count_documents({})
        return count > 0
    except Exception as e:
        return False

def myPOST(image_data, urlDatabase, adName):
    # Chuyển đổi dữ liệu của bức ảnh thành mã base64
    #base64_image = base64.b64encode(image_data).decode("utf-8")
    uri = "mongodb+srv://vuongmongo:dU8JZCbhGJ9M0un1@vuong-iot.ewsddrs.mongodb.net/{urlDatabase}?retryWrites=true&w=majority&appName=Vuong-IoT"
    client = MongoClient(uri)
    db = client[urlDatabase]
    try:
        # Lưu base64 vào collection
        collection = db[adName]
        count = collection.count_documents({}) + 1
        document = {
            "times": count,
            "image": image_data
        }
        #collection.insert_one({"image": base64_image})
        collection.insert_one(document)
        print("----------")
        print("Insert Successfully!")
    except Exception as e:
        print("----------")
        print("Error!!: ", e)

def myGET(urlDatabase, adName):
    uri = "mongodb+srv://vuongmongo:dU8JZCbhGJ9M0un1@vuong-iot.ewsddrs.mongodb.net/{urlDatabase}?retryWrites=true&w=majority&appName=Vuong-IoT"
    if (checkAvailable(uri, urlDatabase, adName)):
        client = MongoClient(uri)
        db = client[urlDatabase]
        collection = db[adName]
        document = collection.find_one({}, sort=[("_id", -1)])
        getImage = document["image"]
        return getImage
    else:
        print("----------")
        print("No DATA!")
        return False

if __name__ == "__main__":
    with open("picture.jpg", "rb") as f:
        image_data = f.read()
        myPOST(image_data, "admin2", "customer1")
