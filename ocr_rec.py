import cv2
import numpy as np


img=cv2.imread('./data/img_0000001.jpg')
rows,cols,ch = img.shape


cv2.imshow('image',img)
cv2.imshow('GRAY',cv2.cvtColor(img,cv2.COLOR_BGR2GRAY))
cv2.imshow('YCR_CB',cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB))
cv2.imshow('HLS',cv2.cvtColor(img,cv2.COLOR_BGR2HLS))
cv2.imshow('HSV',cv2.cvtColor(img,cv2.COLOR_BGR2HSV))
cv2.imshow('LAB',cv2.cvtColor(img,cv2.COLOR_BGR2LAB))
cv2.imshow('LUV',cv2.cvtColor(img,cv2.COLOR_BGR2LUV))
cv2.imshow('XYZ',cv2.cvtColor(img,cv2.COLOR_BGR2XYZ))
cv2.imshow('YUV_IYUV',cv2.cvtColor(img,cv2.COLOR_BGR2YUV_IYUV))


kernel = np.ones((2,2),np.uint8)
cv2.imshow('erosion',cv2.erode(img,kernel,iterations = 1))
cv2.imshow('dilation',cv2.dilate(img,kernel,iterations = 1))
cv2.imshow('opening',cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel))
cv2.imshow('closing',cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel))
cv2.imshow('gradient',cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel))
cv2.imshow('tophat',cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel))


cv2.imshow('GaussianBlur3',cv2.GaussianBlur(img,(3,3),0))
cv2.imshow('GaussianBlur5',cv2.GaussianBlur(img,(5,5),0))
cv2.imshow('GaussianBlur7',cv2.GaussianBlur(img,(7,7),0))
cv2.imshow('blur3',cv2.blur(img, (3,3)))
cv2.imshow('blur5',cv2.blur(img, (5,5)))
cv2.imshow('blur7',cv2.blur(img, (7,7)))
cv2.imshow('GRAY',cv2.cvtColor(img,cv2.COLOR_BGR2GRAY))
cv2.imshow('YCR_CB',cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB))
cv2.imshow('HLS',cv2.cvtColor(img,cv2.COLOR_BGR2HLS))
cv2.imshow('HSV',cv2.cvtColor(img,cv2.COLOR_BGR2HSV))
cv2.imshow('LAB',cv2.cvtColor(img,cv2.COLOR_BGR2LAB))
cv2.imshow('LUV',cv2.cvtColor(img,cv2.COLOR_BGR2LUV))
cv2.imshow('XYZ',cv2.cvtColor(img,cv2.COLOR_BGR2XYZ))
cv2.imshow('YUV_IYUV',cv2.cvtColor(img,cv2.COLOR_BGR2YUV_IYUV))


kernel = np.ones((2,2),np.uint8)
cv2.imshow('erosion',cv2.erode(img,kernel,iterations = 1))
cv2.imshow('dilation',cv2.dilate(img,kernel,iterations = 1))
cv2.imshow('opening',cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel))
cv2.imshow('closing',cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel))
cv2.imshow('gradient',cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel))
cv2.imshow('tophat',cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel))


cv2.imshow('GaussianBlur3',cv2.GaussianBlur(img,(3,3),0))
cv2.imshow('GaussianBlur5',cv2.GaussianBlur(img,(5,5),0))
cv2.imshow('GaussianBlur7',cv2.GaussianBlur(img,(7,7),0))
cv2.imshow('blur3',cv2.blur(img, (3,3)))
cv2.imshow('blur5',cv2.blur(img, (5,5)))
cv2.imshow('blur7',cv2.blur(img, (7,7)))

##########################字体倾斜角度##########################
cv2.imshow('sheare-10',cv2.warpAffine(img, np.array([[1, np.tan(-10 * np.pi / 180), 0],[0, 1, 0]], dtype=np.float32), (cols, rows)))
cv2.imshow('sheare10',cv2.warpAffine(img, np.array([[1, np.tan(10 * np.pi / 180), 0],[0, 1, 0]], dtype=np.float32), (cols, rows)))
################################################################

##########################字体倾斜角度##########################
pts1 = np.float32([[0, 0], [cols, 0], [0, rows]])
pts2 = np.float32([[-cols * 0.02, rows * 0], [cols * 0.98, rows * 0.1], [cols * 0, rows * 1]])
cv2.imshow('image_left', cv2.warpAffine(img, cv2.getAffineTransform(pts1, pts2), (cols, rows)))

pts3 = np.float32([[0, 0], [cols, 0], [0, rows]])
pts4 = np.float32([[cols * 0.02, rows * 0], [cols * 0.98, rows * 0.1], [cols * 0, rows * 1]])
cv2.imshow('image_right', cv2.warpAffine(img, cv2.getAffineTransform(pts3, pts4), (cols, rows)))
################################################################

###########################锐化#################################
def custom_blur_demo(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)  # 锐化
    dst = cv2.filter2D(image, -1, kernel=kernel)
    cv2.imshow("custom_blur_demo", dst)
cv2.imshow("input image", img)
custom_blur_demo(img)
################################################################

cv2.waitKey(0)
