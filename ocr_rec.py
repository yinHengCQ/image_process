import cv2
import numpy as np


img=cv2.imread('./data/img_0000001.jpg')

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


cv2.waitKey(0)
