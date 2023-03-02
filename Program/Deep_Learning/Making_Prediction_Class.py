import cv2
import tensorflow as tf
import os
import numpy as np
import random
from random import seed
from random import randint
import sys
sys.path.append('../')
from Picture_Preprocess.Image_preprocess_class import Image_Preprocess
from Utilities.Stack import Stack
from Utilities.Linear_Queue import Queue
from Utilities.Merge_Sort import *

class Making_Prediction():
    def __init__(self):
        self.CATEGORIES = ["A","A1","B","B1","C","C1","D","D1","E","E1","F","F1","G","G1",
              "H","H1","I","I1","J","J1","K","K1","L","L1","M","M1","N","N1",
              "O","O1","P","P1","Q","Q1","R","R1","S","S1","T","T1",
              "U","U1","V","V1","W","W1","X","X1","Y","Y1","Z","Z1"]
        self.IMG_SIZE = 28
        self.img_pps = Image_Preprocess()
        self.conf_stack = Stack()
        self.Queue_operator = Queue()
        self.predictions_confidence = []
        self.predictions_confidence_list = []
        self.model_num = 0
        self.prepared = None
        
    def prepare(self,filepath):
        self.img_pps.img = cv2.imread(filepath,cv2.IMREAD_GRAYSCALE)
        image_array = np.asarray(self.img_pps.img)
        mean = np.mean(image_array)
        if mean < 100: #Do Thresholding when it's black background
            ret,thresh = cv2.threshold(self.img_pps.img,125,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            self.img_pps.img = thresh #Apply thresholding
        self.img_pps.image_array = self.img_pps.img.tolist()
        #Convert numpy array to list
        cropped = self.img_pps.crop_whole_image(self.img_pps.image_array)
        #Crop the image
        final = self.img_pps.image_resize(cropped,self.IMG_SIZE)
        #Resize image to 28* 28 resolution
        return final.reshape(-1, self.IMG_SIZE, self.IMG_SIZE, 1)

    def make_prediction(self,model_dir):
        #Path is the path to image/images
        model = tf.keras.models.load_model(model_dir)
        prediction = model.predict([self.prepared])
        confidence = prediction.tolist()
        rounded_prediction = [round(x) for x in confidence[0]]
        alphabet_prediction = self.CATEGORIES[(rounded_prediction.index(1))]
        #print("Prediction:\n",alphabet_prediction, "\n\nDir: ", filepath, '\n --------------------------------')
        return [alphabet_prediction,confidence]
    
    def gen_predictions_confidence(self,path):
        #Path is the path to image/images
        current_path = os.path.dirname(__file__)
        #model_folder_path = os.path.relpath('CNN_Models',current_path)
        model_folder_path = ("Deep_Learning\\CNN_Models")
        self.prepared = self.prepare(path)
        for model in os.listdir(model_folder_path):
            #Generate predictions using different models
            self.model_num += 1
            model_path = model_folder_path + "\\" + model #Path to each model
            print("Using ",model," model\n")
            #Objective 4.f
            prediction_confidence = self.make_prediction(model_path)
            self.predictions_confidence.append(prediction_confidence)
            #Each prediction of letter saved in a list attribute
            #Confidence of these predictions saved in another list of corresponding index
        return self.predictions_confidence
    
    def create_confidence_stack(self,list_of_prediction_accuracy):
        #Each element within list should contain the confidence/accuracy of prediction
        self.Queue_operator.alter_size(self.model_num)
        self.conf_stack.alter_size(self.model_num)
        for pair in list_of_prediction_accuracy:
            max_conf = max(pair[1][0])
            self.predictions_confidence_list.append([pair[0],max_conf]) 
            self.Queue_operator.enqueue(max_conf)
            #Enqueue all confidence scores
        print("predictions_confidence_list: ",self.predictions_confidence_list,"\n")
        self.Queue_operator.queue = merge_sort(self.Queue_operator.queue,0,self.Queue_operator.size - 1) #Sort the scores from low to high
        print("Queue: ",self.Queue_operator.queue,"\n")
        for element in self.Queue_operator.queue:
            self.conf_stack.push(self.Queue_operator.dequeue())
            #Push into stack with the top being highes confidence

    def final_prediction(self):
        list_len = len(self.predictions_confidence_list)
        letter_predictions = []
        prediction = "Prediction"
        for item in self.predictions_confidence_list:
            letter_predictions.append(item[0])
        print("Letter_predicions: ",letter_predictions)
        mode = self.find_mode(letter_predictions)
        print("Mode: ",mode)
        print("Stack: ",self.conf_stack.stack)
        if len(mode) == 1:#Majority Voting
            prediction = mode[0]
        elif len(set(self.conf_stack.stack)) == 1:
            #All predictions have same confidence
            seed(1)
            rnd = randint(0,len(mode) -1)
            list_of_mode = [letter for letter in mode]
            for x in range(3):
                random.shuffle(list_of_mode)
                #Prediction would be a random letter within the list
            print("Random integer: ",str(rnd))
            print("Shuffled List: ",list_of_mode)
            prediction = list_of_mode[rnd]
        else:
            greatest_confidence = self.conf_stack.pop()
            #Otherwise final prediction would be the one of highest confidence
            print("Greatest confidence: ",greatest_confidence)
            for pairs in self.predictions_confidence_list:
                if pairs[1] == greatest_confidence:
                    prediction = pairs[0]
                    break
        return prediction
    
    def find_mode(self,list_of_items):
        (values,counts) = np.unique(list_of_items,return_counts = True)
        mode = values[counts == counts.max()]
        return mode
