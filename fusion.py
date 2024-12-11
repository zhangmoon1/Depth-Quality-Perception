import numpy as np
from skimage.metrics import structural_similarity as ssim
from PIL import Image, ImageDraw
import cv2
import os

def read_image_from_txt(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        lines = [line.strip().split() for line in lines]
        image_array = np.array([[int(pixel) for pixel in line] for line in lines])
        #print(image_array)
    return image_array

def get_coordinates_for_class(arr, class_label):#获取坐标位置
    coordinates = np.column_stack(np.where(arr == class_label))
    return coordinates

def get_score_by_id(file_path, target_id):
    # 打开文件
    s=0.0
    with open(file_path, 'r') as file:
        # 逐行读取文件内容
        for line in file:
            #print(line)
            # 切分每行的内容，假设格式是"编号 分数"
            parts = line.strip().split()
            current_id, score = parts
            #print(current_id, score,target_id)
            # 检查当前行的编号是否与目标编号匹配
            if current_id == str(target_id):
                 # 返回对应的分数
                 s=score
    #print(s)
    return s

def apply_color_to_regions(sal1,sal2, regions,score,t):
    score=float(score)
    if score > t:
        for (y,x) in regions:
                #print(x,y)
                sal2[y,x]=sal1[y,x]

    return sal2

RGB_sal='F:/zmy/paper2/data/STERE/BBRF_RGBSal/'
RGBD_sal = 'C:/Users/zhang/Desktop/Experiment/STATE-OF-THE-ART/23/PICR-Net23/PICR-Net/STERE1000/'
RGB_score= 'F:/zmy/paper2/data/STERE/score/'
label_txt='F:/zmy/paper2/data/STERE/region/'
save_path='F:/zmy/paper2/data/STERE/Ablation/Tc/PICRNet/0.3_2/'
t=0.3 #阈值
if not os.path.exists(save_path):
    os.makedirs(os.path.dirname(save_path))
    print('Create!')
for image_name in os.listdir(RGB_sal):

        #print(image_name)
        gt = cv2.imread(RGB_sal+image_name)
        label = read_image_from_txt(label_txt + image_name.replace(".png", '.jpg') + '.txt')  ##区域标签
        # 获取图像中所有类别的列表
        all_classes = np.unique(label)
        sal1 =cv2.imread(RGB_sal + image_name)
        sal2 =cv2.imread(RGBD_sal + image_name)
        for class_label in all_classes:
            coordinates = get_coordinates_for_class(label, class_label)  # 区域坐标
            score = get_score_by_id(RGB_score+image_name+'.txt', class_label)
            sal2 = apply_color_to_regions(sal1,sal2, coordinates, score,t)
        cv2.imwrite(save_path+image_name,sal2)
        print(save_path+image_name)
