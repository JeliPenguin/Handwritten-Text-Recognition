import cv2
import os
import numpy as np

'''from Image_preprocess_class import Image_Preprocess'''

DATADIR = "C:/Users/Jeffrey/Desktop/Dataset/Alphabet/Test Sets/Test_Set_For_Thresholding/"
for imgpath in os.listdir(DATADIR):
    path = DATADIR + imgpath
    image = cv2.imread(path)
    '''print(path)
    cv2.imshow("image",image)
    cv2.waitKey(0)'''
    image_array = np.asarray(image)
    mean = np.mean(image_array)
    if mean < 150:
        print(imgpath ,": Black Background")
    else:
        print(imgpath, ": White Background")
