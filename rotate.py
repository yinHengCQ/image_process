import cv2
from math import *
import numpy as np
import math
from PIL import Image


def rotate(img,args):
    pt1, pt2, pt3, pt4=args
    withRect = math.sqrt((pt4[0] - pt1[0]) ** 2 + (pt4[1] - pt1[1]) ** 2)  # 矩形框的宽度
    angle = acos((pt4[0] - pt1[0]) / withRect) * (180 / math.pi)  # 矩形框旋转角度

    if pt4[1] <= pt1[1]:
        angle = -angle

    height = img.shape[0]  # 原始图像高度
    width = img.shape[1]  # 原始图像宽度
    rotateMat = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)  # 按angle角度旋转图像
    heightNew = int(width * fabs(sin(radians(angle))) + height * fabs(cos(radians(angle))))
    widthNew = int(height * fabs(sin(radians(angle))) + width * fabs(cos(radians(angle))))

    rotateMat[0, 2] += (widthNew - width) / 2
    rotateMat[1, 2] += (heightNew - height) / 2
    imgRotation = cv2.warpAffine(img, rotateMat, (widthNew, heightNew), borderValue=(255, 255, 255))

    # 旋转后图像的四点坐标
    [[pt1[0]], [pt1[1]]] = np.dot(rotateMat, np.array([[pt1[0]], [pt1[1]], [1]]))
    [[pt3[0]], [pt3[1]]] = np.dot(rotateMat, np.array([[pt3[0]], [pt3[1]], [1]]))
    [[pt2[0]], [pt2[1]]] = np.dot(rotateMat, np.array([[pt2[0]], [pt2[1]], [1]]))
    [[pt4[0]], [pt4[1]]] = np.dot(rotateMat, np.array([[pt4[0]], [pt4[1]], [1]]))

    # 处理反转的情况
    if pt2[1] > pt4[1]:
        pt2[1], pt4[1] = pt4[1], pt2[1]
    if pt1[0] > pt3[0]:
        pt1[0], pt3[0] = pt3[0], pt1[0]

    imgOut = imgRotation[int(pt2[1]):int(pt4[1]), int(pt1[0]):int(pt3[0])]
    return imgOut


line="359.01,771.97,348.01,751.97,535.01,638.97,551.01,656.97,*小宅屋*专用盗图可耻"
text_list = line.strip().split(',')
loc = (float(text_list[0]), float(text_list[1]), float(text_list[4]), float(text_list[5]))
print(loc)

if (max([loc[0],loc[2]])/min([loc[0],loc[2]]))>1.2 or ((max([loc[1],loc[3]])/min([loc[1],loc[3]]))>1.2):
    one=[float(i) for i in [text_list[0],text_list[2],text_list[4],text_list[6]]]
    two=[float(i) for i in [text_list[1],text_list[3],text_list[5],text_list[7]]]
    temp_img=rotate(cv2.imread('./data/1.jpg'),map(lambda x,y:[x,y],one,two))
else:
    temp_img=np.asarray(Image.open('./data/1.jpg').crop(loc))

cv2.imwrite('./data/temp_1.jpg',temp_img)
temp_img=Image.fromarray(temp_img)
temp_width=int(32*(temp_img.width/temp_img.height))

cv2.imwrite('./data/out_1.jpg',np.asarray(temp_img.resize((temp_width, 32))))