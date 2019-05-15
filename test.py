import numpy as np
import cv2

im = cv2.imread('target.jpg')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
image, contours= cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
img = cv2.drawContours(im, contours, -1, (0,255,0), 3)
#cnt = contours[4]
#img = cv2.drawContours(img, [cnt], 0, (0,255,0), 3)
img.show()
