import os

def read_txt(filename):
    data = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()  # 分割行，并去除两端的空白字符
            if len(parts) == 2:
                try:
                    key = int(parts[0])  # 尝试将第一个部分转换为整数
                    value = float(parts[1])  # 将第二个部分转换为浮点数
                    data[key] = value
                except ValueError:
                    print("文件格式错误：", line)
    return data

def calculate_difference(data1, data2):
    difference = {}
    for key in data1:
        if key in data2:
            difference[key] = data1[key] - data2[key]
    return difference

def write_txt(filename, data):
    with open(filename, 'w') as file:
        for key, value in data.items():
            file.write(f"{key} {value}\n")

# 读取两个txt文件

file1 = 'F:/zmy/paper2/data/STERE/RGB_Sim/'
file2 = 'F:/zmy/paper2/data/STERE/D_Sim/'

for file_name in os.listdir(file1):
    data1 = read_txt(file1+file_name)
    data2 = read_txt(file2+file_name)
    # 计算数值差
    difference = calculate_difference(data1, data2)

    # 将结果写入新的文本文件
    output_filename = 'F:/zmy/paper2/data/STERE/score/'+file_name
    if not os.path.exists(os.path.dirname(output_filename)):
        os.makedirs(os.path.dirname(output_filename))
    write_txt(output_filename, difference)

    print("数值差已经写入到", output_filename)
