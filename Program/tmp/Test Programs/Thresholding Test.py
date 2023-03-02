import cv2
import os
from Image_preprocess_class import Image_Preprocess

DATADIR = "C:/Users/Jeffrey/Desktop/Dataset/Alphabet/Test_Set_For_AaBbCc/"
path1 = os.path.join(DATADIR,'A/A-0.png')
path2 = os.path.join(DATADIR,'A Lower/hsf_0_00000.png')
img_pps = Image_Preprocess()
img_pps.img = cv2.imread(path1,cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread(path2,cv2.IMREAD_GRAYSCALE)

ret,thresh1 = cv2.threshold(img_pps.img,125,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
ret,thresh2 = cv2.threshold(img2,125,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

cv2.imshow('img1',thresh1)
cv2.imshow('img2',thresh2)
