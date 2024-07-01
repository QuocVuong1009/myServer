#Perfect
from ultralytics import YOLO
import cv2
import numpy as np
import math
import os

def init_preprocess(Path):
    global model
    model = YOLO(Path, "v8")

# Hàm tính góc lệch của ảnh
def calculateAngle(line):
    rect = cv2.minAreaRect(line)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    p1, p2 = box[0], box[1]
    angle = math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))
    return angle

# Hàm xoay ảnh
def rotateImage(angle, image):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    residual = 0.95 - (abs(angle) / 100)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    box = np.array([[0, 0], [w, 0], [w, h], [0, h]])
    rotated_box = cv2.transform(np.array([box]), M)[0]
    x_min = abs(np.min(rotated_box[:, 0]))
    x_max = int(abs(np.max(rotated_box[:, 0]) * residual))
    y_min = abs(np.min(rotated_box[:, 1]))
    y_max = int(abs(np.max(rotated_box[:, 1]) * residual))
    cropped_segment = rotated[y_min:y_max, x_min:x_max]
    return cropped_segment

# Hàm tìm bốn góc của vùng phát hiện
def get_four_corners(mask):
    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        contour = max(contours, key=cv2.contourArea)
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:
            return approx
    return None

# Hàm căn chỉnh và cắt ảnh
def align_and_crop(image, corners):
    pts1 = np.float32([corner[0] for corner in corners])
    rect = np.zeros((4, 2), dtype="float32")
    s = pts1.sum(axis=1)
    rect[0] = pts1[np.argmin(s)]
    rect[2] = pts1[np.argmax(s)]
    diff = np.diff(pts1, axis=1)
    rect[1] = pts1[np.argmin(diff)]
    rect[3] = pts1[np.argmax(diff)]
    (tl, tr, br, bl) = rect
    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    aligned = cv2.warpPerspective(image, M, (maxWidth, maxHeight), flags=cv2.INTER_LANCZOS4)
    return aligned

# Hàm chính của project
def my_main(image):
    H, W, _ = image.shape
    detection_output = model.predict(source=image, save=False)
    for i in detection_output:
        if i.masks is not None:
            for j, mask in enumerate(i.masks.data):
                mask = mask.cpu().numpy() * 255
                mask = cv2.resize(mask, (W, H))
                contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    corners = get_four_corners(mask)
                    if corners is not None:
                        cropped_segment = align_and_crop(image, corners)
                    else:
                        x, y, w, h = cv2.boundingRect(contour)
                        cropped_segment = image[y:y+h, x:x+w]
                        angle = calculateAngle(contour)
                        if angle < -45:
                            angle = (90 + angle)
                        if abs(angle) > 3:
                            cropped_segment = rotateImage(angle, cropped_segment)
                    print("DONE!!!")
                    return cropped_segment
        else:
            print("PLEASE RECAPTURE!!!")

def saveTheFile(base, pic, ad_name):
    if not os.path.exists(base):
        os.makedirs(base)
    # existing_files = [f for f in os.listdir(base) if os.path.isfile(os.path.join(base, f))]
    # num_existing_files = len(existing_files)
    # pic_name = f"pic_{num_existing_files + 1}.jpg"
    # saved_path = os.path.join(base, pic_name)
    # cv2.imwrite(saved_path, pic)
    existing_files = [f for f in os.listdir(base) if os.path.isfile(os.path.join(base, f)) and f.startswith(ad_name)]
    num_existing_files = len(existing_files)
    pic_name = f"{ad_name}{num_existing_files + 1}.jpg"
    saved_path = os.path.join(base, pic_name)
    cv2.imwrite(saved_path, pic)

if __name__ == "__main__":
    image = cv2.imread('anhtestreal/testlc12.jpg')
    my_pic = my_main(image)
    saveTheFile("API_output", my_pic, "vuong")
















   




















   





















   




















   









