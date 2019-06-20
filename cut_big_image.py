import cv2
import numpy as np


origin=cv2.imread("1.jpg")
m=5
n=4

def divide_method1(img,m,n):#分割成m行n列
    h, w = img.shape[0],img.shape[1]
    gx, gy = np.meshgrid(np.linspace(0, w, n), np.linspace(0, h, m))
    gx=np.round(gx).astype(np.int)
    gy=np.round(gy).astype(np.int)

    divide_image = np.zeros([m-1, n-1, int(h*1.0/(m-1)+0.5), int(w*1.0/(n-1)+0.5),3], np.uint8)#这是一个五维的张量，前面两维表示分块后图像的位置（第m行，第n列），后面三维表示每个分块后的图像信息
    for i in range(m-1):
        for j in range(n-1):
            divide_image[i,j,0:gy[i+1][j+1]-gy[i][j], 0:gx[i+1][j+1]-gx[i][j],:]= img[
                gy[i][j]:gy[i+1][j+1], gx[i][j]:gx[i+1][j+1],:]#这样写比a[i,j,...]=要麻烦，但是可以避免网格分块的时候，有些图像块的比其他图像块大一点或者小一点的情况引起程序出错
    return divide_image

def display_blocks(divide_image):#
    m,n=divide_image.shape[0],divide_image.shape[1]
    for i in range(m):
        for j in range(n):
            cv2.imwrite('./temp/{}.jpg'.format(str(i*n+j+1)),divide_image[i,j,:])

def image_concat(divide_image):
    m,n,grid_h, grid_w=[divide_image.shape[0],divide_image.shape[1],#每行，每列的图像块数
                       divide_image.shape[2],divide_image.shape[3]]#每个图像块的尺寸

    restore_image = np.zeros([m*grid_h, n*grid_w, 3], np.uint8)
    for i in range(m):
        for j in range(n):
            restore_image[i*grid_h:(i+1)*grid_h,j*grid_w:(j+1)*grid_w]=divide_image[i,j,:]
    return restore_image


divide_image1=divide_method1(origin,m+1,n+1)#该函数中m+1和n+1表示网格点个数，m和n分别表示分块的块数
display_blocks(divide_image1)
restore_image1=image_concat(divide_image1)
cv2.imwrite('./temp/{}.jpg'.format("restore"),restore_image1)