import os
import cv2
import time
from Image_preprocess_class import Image_Preprocess
files= []

DATADIR = "C:/Users/Jeffrey/Desktop/Dataset/Alphabet/Test_Set_For_AaBbCc/Image_Preprocess_Test_Set/"
files = [f for f in (os.listdir(DATADIR))]
img_pps = Image_Preprocess()
CATEGORIES = ["A","a","B","b","C","c"]
counter = 0
for category in CATEGORIES:
    path = os.path.join(DATADIR,files[counter]) #path to Handwritten alphabet images
    class_label = CATEGORIES.index(category)
    for img in os.listdir(path):
        img_pps.img = cv2.imread(path + '/'+img,cv2.IMREAD_GRAYSCALE)
        if counter%2 == 0:
            ret,thresh = cv2.threshold(img_pps.img,125,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            img_pps.img = thresh
            cv2.imshow('thresh',thresh)
            cv2.waitKey(0)
        img_pps.image_array = img_pps.img.tolist()
        final = img_pps.image_resize(img_pps.crop_whole_image(),28)
        cv2.imshow('final',final)
        cv2.waitKey(0)
    counter += 1
