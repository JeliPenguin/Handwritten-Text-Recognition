import cv2
import tensorflow as tf
import os
import numpy as np
import sys
sys.path.append('../')
from Picture_Preprocess.Image_preprocess_class import Image_Preprocess

CATEGORIES = ["A","A1","B","B1","C","C1","D","D1","E","E1","F","F1","G","G1",
              "H","H1","I","I1","J","J1","K","K1","L","L1","M","M1","N","N1",
              "O","O1","P","P1","Q","Q1","R","R1","S","S1","T","T1",
              "U","U1","V","V1","W","W1","X","X1","Y","Y1","Z","Z1"]
IMG_SIZE = 28
path = "Test_Sets\\"

showinfo = False
img_pps = Image_Preprocess()
model_dir = "CNN_Models\\"
def prepare(filepath):
    img_pps.img = cv2.imread(filepath,cv2.IMREAD_GRAYSCALE)
    image_array = np.asarray(img_pps.img)
    mean = np.mean(image_array)
    if mean < 100: #Do Thresholding when it's black background
        ret,thresh = cv2.threshold(img_pps.img,125,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        img_pps.img = thresh
    img_pps.image_array = img_pps.img.tolist()
    cropped = img_pps.crop_whole_image(img_pps.image_array)
    final = img_pps.image_resize(cropped,IMG_SIZE)
    return final.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

for model in os.listdir(model_dir):
    model_path = model_dir + model
    file = open("Results\\{}_Results.txt".format(model),"w")
    model = tf.keras.models.load_model(model_path)
    for alphabet in os.listdir(path):
        filepath = path + alphabet
        correct = 0
        count = 0
        for image in os.listdir(filepath):
            imagepath = filepath + "\\" + image
            
            prediction = model.predict([prepare(imagepath)])
            orig_prediction = prediction.tolist()
            
            prediction = [round(x) for x in orig_prediction[0]]
            if showinfo:
                print(imagepath)
                print(orig_prediction)
                print("Prediction:\n", CATEGORIES[(prediction.index(1))], "\n\nDir: ", filepath, '\n --------------------------------')
            if alphabet in CATEGORIES[(prediction.index(1))]:
                correct += 1
            count += 1
        writeline = "Category: " + alphabet + " Result: " + str(correct) + "/" + str(count)+ "\n"
        file.write(writeline)

    file.close()

