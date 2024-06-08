from ultralytics import YOLO
import cv2
import numpy as np
import math
import os

# Load YOLO model
# Preprocess_model = YOLO("./models/yolov8_710.pt", "v8")

#Hàm tính góc lệnh của ảnh
def calculateAngle(line):
    # TÍnh khung tối thiểu của bouding box chính ra tính đường viên sát nhất có thể của bpuding box
    rect = cv2.minAreaRect(line)
    box = cv2.boxPoints(rect)
    box = np.int0(box)                
    # Lấy hai điểm đầu tiên từ trên xuống dưới của bouding box
    p1, p2 = box[0], box[1]       
    # Tính góc lệch giữa bouding box và một đường thẳng nằm ngang
    angle = math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))
    return angle

#Hàm xoay ảnh
def rotateImage(angle, image):
    # Lấy tâm của bức ảnh
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    # Tính phần trăm lệch của bức ảnh để triệt tiêu vùng thừa nhất có thể (con số 0.95 được lấy dựa trên rất nhiều lần thử nghiệm)
    residual = 0.95 - (abs(angle)/100)
    # Lấy ma trận 2D của bức ảnh
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # Xoay ảnh dựa trên tâm điểm, góc và ma trận 2D
    rotated = cv2.warpAffine(image, M, (w, h), flags = cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    # Tính toán tọa độ mới của các đỉnh sau khi xoay
    box = np.array([[0, 0], [w, 0], [w, h], [0, h]])
    rotated_box = cv2.transform(np.array([box]), M)[0]
    x_min = abs(np.min(rotated_box[:, 0]))
    x_max = int(abs(np.max(rotated_box[:, 0]) * residual))
    y_min = abs(np.min(rotated_box[:, 1]))
    y_max = int(abs(np.max(rotated_box[:, 1]) * residual))
    # Cắt vùng quan tâm từ ảnh gốc
    cropped_segment = rotated[y_min:y_max, x_min:x_max]
    return cropped_segment

# Hàm chính của project
def my_main(image):
    H, W, _ = image.shape
    # Sử dụng mô hinhg YOLOv8 để dự đoán bức ảnh
    detection_output = Preprocess_model.predict(source=image, save=False)
    for i in detection_output:
        if i.masks is not None:
            for j, mask in enumerate(i.masks.data):
                # Lấy tọa vùng đã được dự đoán
                mask = mask.cpu().numpy() * 255
                mask = cv2.resize(mask, (W, H))
                # Tính toán đường viền của vùng đã được dự đoán
                contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    # Lấy tọa độ 4 điểm của đường viền
                    x, y, w, h = cv2.boundingRect(contour)
                    cropped_segment = image[y:y+h, x:x+w]
                    # Tính toán góc lệch của bức ảnh dựa trên hàm đã viết sau đó thực hiện đổi lại góc cho đúng với thực tế
                    angle = calculateAngle(contour)
                    if (angle < -45):
                        angle = (90 + angle)
                    if (abs(angle) > 3):
                        cropped_segment = rotateImage(angle, cropped_segment)
                    # Định hình lại bức ảnh
                    cropped_segment = cv2.resize(cropped_segment, (480, 640))
                    print("DONE!!! PRE")
                    return cropped_segment
        else:
            print("PLEASE RECAPTURE!!! PRE")

def saveTheFile(base, pic):
    # Kiểm tra xem thư mục base đã tồn tại chưa
    if not os.path.exists(base):
        # Nếu chưa tồn tại, tạo thư mục base
        os.makedirs(base)
    # Liệt kê tất cả những file đã tồn tại ở trong folder
    existing_files = [f for f in os.listdir(base) if os.path.isfile(os.path.join(base, f))]
    # Lấy số lượng các file đã có mặt ở trong folder
    num_existing_files = len(existing_files)
    # Đặt tên file bằng cú pháp "pic_" và sau đó là số lượng file đã tồn tại + 1
    pic_name = f"pic_{num_existing_files + 1}.jpg"
    saved_path = os.path.join(base, pic_name)
    cv2.imwrite(saved_path, pic)

def init_preprocess(Path):
    global Preprocess_model
    Preprocess_model = YOLO(Path, "v8")

if __name__ == "__main__":
    image = cv2.imread('input_pics/pic12.jpg')
    my_pic = my_main(image)
    # saveTheFile("API_output", my_pic)
    cv2.imshow("KQ", my_pic)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
















   




















   





















   




















   









