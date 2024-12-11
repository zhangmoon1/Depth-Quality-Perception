from PIL import Image, ImageDraw
import numpy as np

def read_image_from_txt(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        lines = [line.strip().split() for line in lines]
        image_array = np.array([[int(pixel) for pixel in line] for line in lines])
    return image_array

def get_coordinates_for_class(arr, class_label):
    coordinates = np.column_stack(np.where(arr == class_label))
    return coordinates



def get_score_by_id(file_path, target_id):
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            current_id, score = parts
            if current_id == str(target_id):
                return score
    return None

# 示例用法
file_path_txt = 'F:/zmy/paper2/data/NJU2K/region/000315_left.jpg.txt'
sal_path = 'F:/zmy/paper2/data/NJU2K/SLIC/000315_left.jpg'
score_path = 'F:/zmy/paper2/data/NJU2K/000315_left.png.txt'
output_path = 'F:/zmy/paper2/data/NJU2K/000315_left.jpg'

# 读取标签图像和得分文件
label = read_image_from_txt(file_path_txt)  # 区域标签
all_classes = np.unique(label)

# 读取源图像
image = Image.open(sal_path).convert("RGB")

# 创建一个绘图对象
draw = ImageDraw.Draw(image)

# 为每个类别获取得分并更新图像
for class_label in all_classes:
    coordinates = get_coordinates_for_class(label, class_label)  # 区域坐标
    score = get_score_by_id(score_path, class_label)
    if score is not None:
        score_float = float(score)
    else:
        score_float = 0.0
    # 将score转为浮点数


    # 指定一个常数，例如1，然后减去得分并乘以缩放因子

    brightness =score_float
    print(class_label,brightness)

    #brightness =score_float
    scaled_brightness = int(brightness * 255)

    # 在这里修改图像像素，根据你的需求进行调整
    # for coord in coordinates:
    #     y,x = coord
    #
    #     current_color = image.getpixel((x, y))
    #     updated_color = (#更改为该像素*score+周围像素和对应分数的和
    #         int(current_color[0] * brightness*2),
    #         int(current_color[1] * brightness*2),
    #         int(current_color[2] * brightness*2)
    #     )
    #     image.putpixel((x, y), updated_color)

    label_text = f"{class_label}"
    score_text = f"{score}"
    if score_text !='0.0':
     draw.text((min(coordinates[:, 1]), min(coordinates[:, 0])), label_text, fill=(0, 255, 255))
     #draw.text((min(coordinates[:, 1]), min(coordinates[:, 0]) + 15), score_text, fill=(255, 255, 255))
    # 在图像上绘制标签和分数
    #label_text = f"{class_label}"
    #score_text = f"{score}"

    #draw.text((min(coordinates[:, 1]), min(coordinates[:, 0])), label_text, fill=(255, 255, 255))
    #draw.text((min(coordinates[:, 1]), min(coordinates[:, 0]) + 15), score_text, fill=(255, 255, 255))

# 保存最终图像
image.save(output_path)