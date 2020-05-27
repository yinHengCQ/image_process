import cv2
import random
from math import *
from glob import glob


angle_set=list(set([i for i in range(-20,21)])-set([0]))


def rotate_xy(x, y, angle, cx, cy):
    angle = angle * pi / 180
    x_new = (x - cx) * cos(angle) - (y - cy) * sin(angle) + cx
    y_new = (x - cx) * sin(angle) + (y - cy) * cos(angle) + cy
    return x_new,y_new


def convert_point(landmark, angle, cx, cy):
    landmark = [i for i in zip([landmark[ind_0] for ind_0 in range(0, 8, 2)], [landmark[ind_0] for ind_0 in range(1, 9, 2)])]
    out=[]
    for i,j in landmark:
        x,y=rotate_xy(i,j,angle,cx,cy)
        out.append(x)
        out.append(y)
    return out


def convert_img(img_path,txt_path,txt_name):
    img = cv2.imread(img_path)
    h_origin, w_origin, c = img.shape
    img=cv2.copyMakeBorder(img,h_origin,h_origin,w_origin,w_origin,cv2.BORDER_CONSTANT,value=0)
    h, w, c = img.shape
    angle = random.choice(angle_set)
    center = (h * 0.5, w * 0.5)
    rot_mat = cv2.getRotationMatrix2D(center, angle, 1)
    img_rotated_by_alpha = cv2.warpAffine(img, rot_mat, (w, h))
    cv2.imwrite("D:/all_data/ocr1/image_train_random_rotate/{}_convert.jpg".format(txt_name), img_rotated_by_alpha)

    convert_txt=""
    with open(txt_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            if line == '':
                continue
            points = []
            for ind,p in enumerate([int(float(v)) for v in line.split(',')[:8]]):
                if ind%2==0:
                    points.append(p+w_origin)
                else:
                    points.append(p +h_origin)
            points = convert_point(points, -angle, center[0], center[1])
            convert_txt += "{},{}\n".format(",".join(str(p) for p in points), ",".join(line.split(',')[8:]))

    with open("D:/all_data/ocr1/txt_train_random_rotate/{}_convert.txt".format(txt_name), "w", encoding="utf-8") as f:
        f.write(convert_txt)


def convert_batch_imgs(img_file,txt_file):
    flag=0
    for img_file in glob("{}/*.*".format(img_file)):
        img_name=img_file.split("\\")[-1][:-4]
        flag+=1
        txt_path="{}/{}.txt".format(txt_file,img_name)
        convert_img(img_file,txt_path,img_name)
        print(flag)


convert_batch_imgs("D:/all_data/ocr1/image_train","D:/all_data/ocr1/txt_train")





