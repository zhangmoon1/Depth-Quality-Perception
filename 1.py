import numpy as np
from skimage.metrics import structural_similarity as ssim
import time
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




class ImageProcessing:
    def __init__(self, saliency_map, gt_map):
        self.saliency_map = saliency_map
        self.gt_map = gt_map

    def calculate_s_measure(self, coordinates):
        alpha = 0.5  # 根据需要调整的参数
        beta = 0.5  # 根据需要调整的参数

        s_measure_sum = 0.0

        for x, y in coordinates:
            # 获取显著性图值
            saliency_value = self.saliency_map[x, y]

            # 获取GT图值
            gt_value = self.gt_map[x, y]

            # 计算结构相似性度量 S-measure
            numerator = 2 * saliency_value * gt_value + alpha
            denominator = saliency_value**2 + gt_value**2 + beta
            pixel_s_measure = numerator / denominator
            if pixel_s_measure[0]<=1:
                s_measure_sum += pixel_s_measure[0]

        # 计算平均 S-measure
        # print(s_measure_sum)
        # print(len(coordinates))
        # print(coordinates)
        average_s_measure = s_measure_sum/ len(coordinates)
        return average_s_measure

# 读取两个图像的类别信息

label_path= 'F:/zmy/paper2/data/STERE/region/'  # 替换为你的真实标签文件路径
sal_path='F:/zmy/paper2/data/STERE/BBRF_DSal/'
pgt_path='F:/zmy/paper2/data/STERE/PGT/'
cal_path='F:/zmy/paper2/data/STERE/D_Sim/'
if not os.path.exists(os.path.dirname(cal_path)):
    os.makedirs(os.path.dirname(cal_path))
for image_name in os.listdir(pgt_path):
    if os.path.exists(cal_path+image_name+'.txt'):
        # 如果文件存在，则运行你的代码
        print(image_name)
    else:
        start_time = time.perf_counter()
        gt = cv2.imread(pgt_path+image_name)
        label = read_image_from_txt(label_path+image_name.replace(".png",'.jpg')+'.txt')  ##区域标签
        # 获取图像中所有类别的列表
        all_classes = np.unique(label)
        # print(all_classes)
        # 计算每个类别的 S-measure
        with open(cal_path+image_name+'.txt', "w") as file:
            for class_label in all_classes:
                    coordinates=get_coordinates_for_class(label, class_label)#区域坐标
                    #print(coordinates)
                    array = []
                    pred_path=sal_path+'/'+image_name
                    #print(pred_path)
                    pred = cv2.imread(pred_path)
                    image_processor = ImageProcessing(pred, gt)# 创建 ImageProcessing 对象
                    s_measure = image_processor.calculate_s_measure(coordinates)# 计算 S-measure
                    array.append("{:.4f}".format(s_measure))
                    print(class_label,array)
                    file.write(str(class_label))
                    file.write(" ")
                    file.write(" ".join(map(str, array)))
                    file.write('\n')



