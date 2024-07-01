#NEWWW
import cv2
import csv
import json
import os
import re
import unicodedata
from preProcess import my_main, saveTheFile

def compare_strings(str1, str2, index):
    str1 = str1.lower()
    str2 = str2.lower()
    count = 0
    str2_words = str2.split()
    if len(str2_words) > index:
        str2_word = str2_words[index]
    else:
        str2_word = str2
    if len(str1) != len(str2_word):
        return False
    for i in range(len(str1)):
        if str1[i] == str2_word[i]:
            count += 1
    ratio = count / len(str2_word)
    # if ratio >= 1:
    if ratio >= 0.85:
        return True
    return False

def read_csv_file(csv_file_path):
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            return list(reader), header
    except FileNotFoundError:
        print(f"Error: File not found at {csv_file_path}")
        return None, None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None

# #Hiệu Suất Vương
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def convert_pattern(json_file_path):
    # Đọc dữ liệu từ JSON file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    # Đọc dữ liệu từ CSV file
    reader, header = read_csv_file(csv_file_path_p)
    if not reader or not header:
        return None
    text_column_index = header.index('TenThuoc')
    # Tạo một dictionary để lưu các dữ liệu đã chuyển đổi
    converted_data = {}
    # Tạo một mapping từ chuỗi không dấu đến chuỗi có dấu
    mapping = {}
    for row in reader:
        csv_value = row[text_column_index]
        csv_value_no_accents = remove_accents(csv_value.lower())
        mapping[csv_value_no_accents] = csv_value
    # So sánh và chuyển đổi dữ liệu
    for key, value in json_data.items():
        value_no_accents = remove_accents(value.lower())
        best_match = mapping.get(value_no_accents, value)  # Sử dụng giá trị gốc nếu không tìm thấy khớp
        converted_data[key] = best_match
    # Ghi dữ liệu đã chuyển đổi vào JSON file mới
    converted_json_file_path = json_file_path.replace(".json", "_converted.json")
    try:
        with open(converted_json_file_path, 'w', encoding='utf-8') as file:
            json.dump(converted_data, file, ensure_ascii=False)#, indent=4)
    except Exception as e: 
        print(f"Error: {str(e)}")
        return None
    # Đọc và in nội dung file đã chuyển đổi để kiểm tra
    try:
        with open(converted_json_file_path, "r", encoding='utf-8') as file:
            data = json.load(file)
        result = json.dumps(data, ensure_ascii=False)#, indent=4)
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    # Xóa cả hai file sau khi hoàn tất
    try:
        if os.path.exists(json_file_path):
            os.remove(json_file_path)
        if os.path.exists(converted_json_file_path):
            os.remove(converted_json_file_path)
    except Exception as e:
        print(f"Error while deleting files: {str(e)}")
    return result

def get_matching_rows(input_text, matching_rows, index, count_split, count_text, count_text_2):
    if input_text != "":
        reader, header = read_csv_file(csv_file_path)
        text_column_index = header.index('TenThuoc')
        if count_split == 0:
            one_row = []
            for row in reader:
                if compare_strings(input_text, row[text_column_index], index):
                    matching_rows.append(row)
            for row_f in matching_rows:
                if len(row_f[text_column_index].split()) == 1:
                    one_row.append(row_f)
                    success = save_to_json(one_row, json_file_path)
                    if success:
                        one_row.clear()
        else:
            new_matching_rows = []
            new_matching_rows_2 = []
            for row_2 in matching_rows:
                if compare_strings(input_text, row_2[text_column_index], index):
                    new_matching_rows.append(row_2)
            matching_rows = [row_text for row_text in matching_rows if row_text in new_matching_rows]
            if len(new_matching_rows) == 0:
                for r in reader:
                    if compare_strings(input_text, r[text_column_index], 0):
                        if len(r[text_column_index].split()) == 1 and len(new_matching_rows) == 1:
                            new_matching_rows.append(r)
                        else:
                            new_matching_rows_2.append(r)
                            count_split = 0
                            index = 0
                            count_text = 0
            if new_matching_rows_2:
                matching_rows = new_matching_rows_2.copy()
                new_matching_rows_2.clear()
            else:
                matching_rows = new_matching_rows.copy()
            for row_3 in matching_rows:
                if len(matching_rows) == 1 and index == len(row_3[text_column_index].split()) - 1:
                    success = save_to_json(matching_rows, json_file_path)
                    if success:
                        matching_rows.clear()
        if len(matching_rows) == 0:
            count_split = 0
            index = 0
            count_text = 0
        else:
            count_split += 1
            index += 1
            count_text += 1
    else:
        matching_rows = []
        count_split = 0
        index = 0
        count_text = 0
        count_text_2 = 0
    return matching_rows, count_split, index, count_text, count_text_2
# # ##End Hiệu Suất Vương

def save_to_json(matching_rows_2, json_file_path):
    drug_dict = {}
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
    if os.path.exists(json_file_path):
        try:
            if os.path.getsize(json_file_path) == 0:
                drug_dict = {}
            else:
                with open(json_file_path, 'r', encoding='utf-8') as json_file:
                    drug_dict = json.load(json_file)
        except json.JSONDecodeError as e:
            drug_dict = {}
        except Exception as e:
            drug_dict = {}
    existing_values = set(drug_dict.values())
    max_index = 0
    for key in drug_dict.keys():
        if key.startswith('presName'):
            try:
                index = int(key[8:])
                if index > max_index:
                    max_index = index
            except ValueError:
                pass
    for row in matching_rows_2:
        if row[0] not in existing_values:
            max_index += 1
            drug_dict[f'presName{max_index}'] = row[0]
            existing_values.add(row[0])
    try:
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(drug_dict, json_file, ensure_ascii=False)#, indent=4)
        return True
    except Exception as e:
        return False

def detect_text(results):
    listName = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', ',', 'D', 'Đ', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', '+', 'd', '.', 'đ', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', ')', '(', 'o', 'p', '%', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for result in results:
        bb_list = result.cpu().boxes.numpy()  # Chuyển tensor sang CPU
        center_list = []
        y_sum = 0
        for bb in bb_list:
            xyxy = bb.xyxy
            x_c = (xyxy[0][0] + xyxy[0][2]) / 2
            y_c = (xyxy[0][1] + xyxy[0][3]) / 2
            cls = bb.cls
            y_sum += y_c
            center_list.append([x_c, y_c, listName[int(cls[0])]])
        if len(center_list) <= 0:
            return ""
        l_point = center_list[0]
        r_point = center_list[0]
        for cp in center_list:
            if cp[0] < l_point[0]:
                l_point = cp
            if cp[0] > r_point[0]:
                r_point = cp
        text = ""
        for i, l in enumerate(sorted(center_list, key=lambda x: x[0])):
            text += str(l[2])
        print("Done detect text")
        return text
        
def read_by_line(results, image, json_string, model_2):
    matching_rows = []
    count_split = 0
    index = 0
    count_text = 0
    count_text_2 = 0
    center_line = []
    center_list = []
    min_center_x = float('inf')
    min_center_y = float('inf')
    count_line = 0
    bb_list = []
    json_string = ""
    for reslut in results:
        bb_list = reslut.cpu().boxes.numpy()  # Chuyển tensor sang CPU
        for bb in bb_list:
            xyxy = bb.xyxy
            x_c = (xyxy[0][0] + xyxy[0][2]) / 2
            y_c = (xyxy[0][1] + xyxy[0][3]) / 2
            center_list.append([x_c, y_c])
    center_list = sorted(center_list, key=lambda x: x[1])
    for ct in center_list:
        min_center_x = center_list[count_line][0]
        min_center_y = center_list[count_line][1]
        for ct_2 in center_list:
            if abs(ct_2[1] - min_center_y) < 15:
                center_line.append(ct_2)
        center_line = sorted(center_line, key=lambda x: x[0])
        for ct in center_line:
            if ct in center_list:
                center_list.remove(ct)
        for ct_3 in center_line:
            for box in bb_list:
                if ct_3[0] == (box.xyxy[0][0] + box.xyxy[0][2]) / 2 and ct_3[1] == (box.xyxy[0][1] + box.xyxy[0][3]) / 2:
                    box_int = box.xyxy.astype(int)
                    cv2.rectangle(image, (box_int[0][0], box_int[0][1]), (box_int[0][2], box_int[0][3]),
                                  (255, 0, 255), 1)
                    crop_img = image[box_int[0][1]:box_int[0][3], box_int[0][0]:box_int[0][2]]
                    crop_img = cv2.resize(crop_img, (640, 640))
                    results_2 = model_2(crop_img, imgsz=640, iou=0.25)
                    text = detect_text(results_2)
                    text = text.replace("(", "")
                    text = text.replace(")", "")
                    text = text.strip("()")
                    text = text.replace(".", "")
                    matching_rows, count_split, index, count_text, count_text_2 = get_matching_rows(text, matching_rows, index, count_split, count_text, count_text_2)
        center_line.clear()
    json_string = convert_pattern(json_file_path) #Hiệu Suất Vương
    # json_string = convert_and_delete_json(json_file_path) #Hiệu Suất Việt
    return json_string

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def update_json_file_path(name):
    global json_file_path
    json_file_path = f"./result/{name}.json"
    create_directory_if_not_exists(os.path.dirname(json_file_path))

def init_extract(Path1, Path2):
    global csv_file_path
    global csv_file_path_p
    csv_file_path = Path1  # Path 1: "./DrugDatabase/uniqueNone.csv"
    csv_file_path_p = Path2 # Path 1: "./DrugDatabase/unique.csv"

def extract_main(image, model, model_2, ad_name):    
    json_string = ""
    update_json_file_path(ad_name)
    print("File json la: ", json_file_path)
    image = my_main(image)
    saveTheFile("uploaded_images", image, ad_name)
    results = model(image, imgsz=640, iou=0.25)
    json_string = read_by_line(results, image, json_string, model_2)
    print("EXTRACTING SUCCESSFULLY!!")
    return json_string

if __name__ == "__main__":
    image = cv2.imread("anhtest60.jpg")
    result = extract_main(image)
    print("Cuoi cung ket qua la: ", result)





