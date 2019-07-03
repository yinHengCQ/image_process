from PIL import Image
import cv2
import numpy as np


# img=Image.open("./1_new.jpg")
# cv2.imshow('11',np.asanyarray(img.rotate(-90, expand = 1)))
# cv2.waitKey(0)

# temp=dict()
# with open("./sample_task1.txt","r",encoding="utf-8") as f:
#     for line in f.readlines():
#         vv = line.strip().split(".jpg")
#         temp[vv[0]] = vv[1].strip()
#
# out=""
# for i in sorted(temp.items(),key=lambda x:int(x[0][5:])):
#     out+="{} {}\n".format(i[0],i[1])
#
# with open("./out.txt","w",encoding="utf-8") as f:
#     f.write(out)

# img=cv2.imread("./1_new.jpg")
# img=cv2.imread('./data/img_0000001.jpg')
# rows,cols,ch = img.shape

# pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
# pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])
#
# M = cv2.getPerspectiveTransform(pts1,pts2)
#
# dst = cv2.warpPerspective(img,M,(300,300))

# print(rows)
# print(cols)
# pts1 = np.float32([[0,5],[282,5],[5,282]])
# pts2 = np.float32([[0,0],[282,0],[0,282]])
#
# M = cv2.getAffineTransform(pts1,pts2)
#
# dst = cv2.warpAffine(img,M,(cols,rows))
#
# cv2.imshow('input',img)
# cv2.imshow('output',dst)

# cv2.waitKey(0)


img = cv2.imread('./data/img_0000001.jpg')
rows, cols, ch = img.shape

pts1 = np.float32([[0, 0], [cols - 1, 0], [0, rows - 1]])
pts2 = np.float32([[cols * 0.2, rows * 0.1], [cols * 0.9, rows * 0.2], [cols * 0.1, rows * 0.9]])
cv2.imshow('image1', cv2.warpAffine(img, cv2.getAffineTransform(pts1, pts2), (cols, rows)))

pts3 = np.float32([[0, 0], [cols - 1, 0], [0, rows - 1]])
pts4 = np.float32([[cols * 0.1, rows * 0.1], [cols * 0.98, rows * 0.2], [cols * 0.02, rows * 0.9]])
cv2.imshow('image2', cv2.warpAffine(img, cv2.getAffineTransform(pts3, pts4), (cols, rows)))


k = cv2.waitKey(0)

