import numpy as np
import cv2
from PIL import Image
import pylab as pl
from math import *
from statistics import *
from matplotlib import *
############################################

#convert the image into gray scale
im_gray = cv2.imread('franco.jpg', cv2.IMREAD_GRAYSCALE)
imgsize=im_gray.shape #image size(length,width)
width=imgsize[1]  # width of the image
length=imgsize[0] # lenght of image
print(width)
print (length)
#convert dray scale image into binary image
(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
MAP = np.array(im_bw)
print(thresh) # threshold of the binary image
#conver int matrix of 0 (spaces or white) & 1(obstcaleor black)
for i in range(width):
    for k in range (length):
        if MAP[k][i]>= thresh:
           MAP[k][i] = 0
        else :
           MAP[k][i]=1
print(MAP)
    



        



