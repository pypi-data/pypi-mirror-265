import cv2
import time
import os
import sys
import importlib
import time
import shutil
from tqdm import tqdm
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_PATH)
sys.path.append(BASE_PATH)
importlib.reload(sys)
from YoloV5Detector.V5Detector import Detector
import numpy as np
import functions

def robotcamchange(pixel_x,pixel_y,pixel_z):

    transform_matrix = np.array([
                                    [-9.98681177e-01,  1.05280144e-02,  5.02500545e-02, - 2.97004394e+02],
                                    [8.78909685e-03,  9.99359067e-01, - 3.47016746e-02, - 4.26915313e+02],
                                [-5.05831873e-02, - 3.42142567e-02, - 9.98133621e-01, 7.27910090e+02],
        [0, 0, 0, 1]
    ])
    transform_matrixT = np.linalg.inv(transform_matrix)

    # 相机内参
    camera_matrix = np.array([[3.56424111e+03, 0.00000000e+00, 1.64282247e+03],
                              [0.00000000e+00, 3.56133420e+03, 1.09901305e+03],
                              [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

    # 相机内参求逆
    camera_matrix2 = np.linalg.inv(camera_matrix)
    # 像素坐标变为向量形式
    pixel_coordinates = np.array([[pixel_x * pixel_z], [pixel_y * pixel_z], [pixel_z]])
    # 将相机内参逆矩阵点成像素坐标
    T2 = np.dot(camera_matrix2, pixel_coordinates)
    # 在T2基础上添加一行[1]使其变成4*1矩阵
    T3 = np.vstack([T2, [1]])
    # 转换矩阵的逆乘T3得到机械臂坐标
    robot_coordinates = np.dot(transform_matrixT, T3)
    #
    x = float(robot_coordinates[0])
    y = float(robot_coordinates[1])
    z = float(robot_coordinates[2])

    data1 = [x,y,150,0,-3.15,0]
    data2 = [x,y,0,0,-3.15,0]

    return data1,data2

def inference_single_image(weights_path, thresh, src_img, cls, colors=None, gpu_id="cpu"):
    det = Detector(weights_path, gpu_id=gpu_id, colors=colors)
    t1 = time.time()
    img = cv2.imread(src_img)
    img_res, det_res = det.detect(img, cls, thresh)
    t2 = (time.time() - t1) * 1000
    img_res = det.draw_box(img, det_res)
    det.print_result(det_res)
    centerx,centery = det.print_result(det_res)
    # 打印检测结果
    return centerx,centery
    # cv2.imwrite(dst_img, img_res)

def get_images_from_dir(imgPath):
    imagelist = os.listdir(imgPath)
    image_dic = []
    for imgname in imagelist:
        if (imgname.endswith(".jpg")):
            imgp = imgPath + imgname
            image_dic.append(imgp)
    return image_dic


import urllib.request


def download_bmp_image(url, local_filename):
    # 定义要下载的远程BMP图像的URL
    remote_url = url

    # 指定本地保存的文件名
    if not local_filename.endswith('.bmp'):
        local_filename += '.bmp'  # 如果没有提供bmp后缀，则添加上

    try:
        # 创建并打开本地文件以写入
        with open(local_filename, 'wb') as f:
            # 发送HTTP请求获取远程文件
            response = urllib.request.urlopen(remote_url)

            # 将远程文件的内容写入本地文件
            f.write(response.read())

        print(f"成功下载图片至 {local_filename}")
    except urllib.error.HTTPError as e:
        print(f"下载失败：HTTP错误 - {e.code}")
    except urllib.error.URLError as e:
        print(f"下载失败：URL错误 - {e.reason}")
    except Exception as e:
        print(f"下载过程中发生错误：{e}")



def detect(data):
    download_bmp_image(data["path"], 'image.bmp')
    weights_path = "weights/best.pt"
    #设置模型阈值
    thresh = 0.3
    #设置待检测图片
    src_img = 'image.bmp'
    #设置待检测类别名称，不在此列内的物体不会被检测
    # cls = ['mango', 'pomegranate', 'banana', 'green apple',"apple","carambola","orange","Snake fruit","tangerine","mangosteen"]
    cls = data['object']
    #设置待检测类别id对应的BGR颜色，若不设置则随机
    colors = {0: (0, 0, 255), 5: (0, 255, 0)}
    #设置使用第几块cpu序号，可设为'cpu'来使用cpu推理，若不设置，默认使用0号gpu
    gpu_id = 'cpu'
    centerx,centery = inference_single_image(weights_path, thresh, src_img, cls, colors, gpu_id)
    pos1, pos2 = robotcamchange(centerx,centery, 7.27910090e+02)

    return {"msg": "success", "data": {"pos1": pos1, "pos2": pos2}}


if __name__ == '__main__':

    data = {
        "path":"http://8.134.85.230:9000/isdp000000/componentImage/ColorImage_20240328151547.bmp",
        "object":"banana"
    }
    print(detect(data))


