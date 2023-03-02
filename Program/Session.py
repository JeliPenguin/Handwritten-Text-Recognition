from GUI.User_Interface import GUI
#from Picture_Preprocess.Image_preprocess_class import Image_Preprocess
from Picture_Preprocess.Image_preprocess_class import Image_Preprocess
from Deep_Learning.Making_Prediction_Class import Making_Prediction
from tkinter import *
import time
import datetime
import cv2
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt

class Session():
    def __init__(self):
        self.image_path = ''
        self.operation_type = ''
        self.img_pps = Image_Preprocess()
        self.now = datetime.datetime.now()
        self.datapaths = {'SESSION':'Sessions\\',
                          'ROI_PATH':'ROI_Images',
                          'FINAL_PATH':'Final_Images',
                          'CURSESSION':'' #Directory for current session
                          }
        self.Firsttime = True
    def startup_window(self):
        root = Tk()
        sizes = self.determine_Window_size(root)
        window_pos = self.position_window(sizes)
        root.geometry("205x210") #Decides frame dimensions
        root.geometry("+{}+{}".format(window_pos[0],window_pos[1])) 
        root.resizable(False,False)
        app = GUI(window_pos,root)
        root.mainloop()
        self.image_path = app.return_image_directory() #Filepath of image file
        self.operation_type = app.return_operation_type()
        time.sleep(1)
    def determine_Window_size(self,root):
        win_width = root.winfo_reqwidth()
        win_height = root.winfo_reqheight()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        return_list = [[win_width,screen_width],[win_height,screen_height]]
        return return_list
    def position_window(self,sizes):
        info = sizes
        x_pos = int(info[0][1]/2 - info[0][0]/2)
        y_pos = int(info[1][1]/2 - info[1][0]/2)
        return [x_pos,y_pos]
    def update_time(self):
        self.now = datetime.datetime.now()
        self.datapaths['CURSESSION'] = 'Session-{now}\\'.format(now = self.now.strftime('%Y-%m-%d_%H-%M-%S'))
    def create_folder_structure(self):
        session = self.datapaths['SESSION']
        if not os.path.exists(session):
            os.mkdir(session)
        if len([name for name in os.listdir(session)
                if os.path.isdir(os.path.join(session,name))]) > 10:
            noerror = False
            while noerror == False:
                try:
                    shutil.rmtree(session)#Removes all session if there are more than 5 sessions
                    os.mkdir(session)
                    print('Trying')
                    noerror = True
                except:
                    pass
        self.update_time()
        current_session = os.path.join(session,self.datapaths['CURSESSION'])
        roi_path =os.path.join(current_session,self.datapaths['ROI_PATH'])
        final_path = os.path.join(current_session,self.datapaths['FINAL_PATH'])
        if not os.path.exists(current_session):
            os.mkdir(current_session)
            os.mkdir(roi_path)
            os.mkdir(final_path)
        return [roi_path,final_path]

    def preprocess_image(self,image_path,folder_structure):
        roi_final = folder_structure #index 0 to ROI folder, index 1 to Final folder
        #self.img_pps.reset()
        self.img_pps.read_image(image_path)
        if self.Firsttime:
            print("First Time")
            self.img_pps.img = self.img_pps.Remove_Shadow(self.img_pps.img)
            self.Firsttime = False
        operated_image = self.img_pps.Pre_operations(self.img_pps.img)
        if self.operation_type == 'Single':
            self.img_pps.preprocess_img(roi_final[1])
        elif self.operation_type == 'Entire':
            self.img_pps.find_ROI(operated_image,roi_final[0])
            self.operation_type = 'Single'
            for element in os.listdir(roi_final[0]):
                path_to_element = roi_final[0] + ('\\' + element)
                self.preprocess_image(path_to_element,roi_final) #Recursion
        else:
            print('An error has occured, restarting program')
            #self.operation_type = 'Error'
        
    def CNN_prediction(self,folder_structure):
        final_path = folder_structure[1]
        for image_path in os.listdir(final_path):
            prediction_maker = Making_Prediction()
            final_image_path = final_path + "\\" + image_path
            alph_conf_list = prediction_maker.gen_predictions_confidence(final_image_path)
            prediction_maker.create_confidence_stack(alph_conf_list)
            print("Image_path: ",final_image_path)
            print(prediction_maker.final_prediction())
            image = cv2.imread(final_image_path)
            cv2.imshow('img',image)
            cv2.waitKey(0)
