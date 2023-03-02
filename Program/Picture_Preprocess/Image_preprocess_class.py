import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import time

class Image_Preprocess():
    def __init__(self):
        self.DATADIR = ''
        self.img = None
        self.image_array = []
        self.thresh_value = 0
        self.count = 1
        self.image_datas = []
        
    def read_image(self,DATADIR):
        self.DATADIR = DATADIR
        self.img = cv2.imread(self.DATADIR)

    #Objective 2.d
    def Remove_Shadow(self, image):
        #https://stackoverflow.com/questions/44752240/how-to-remove-shadow-from-scanned-images-using-opencv
        rgb_planes = cv2.split(image)
        result_planes = []
        result_norm_planes = []
        for plane in rgb_planes:
            dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
            bg_img = cv2.medianBlur(dilated_img, 21)
            diff_img = 255 - cv2.absdiff(plane, bg_img)
            norm_img = cv2.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
            result_planes.append(diff_img)
            result_norm_planes.append(norm_img)
        result = cv2.merge(result_planes)
        return cv2.merge(result_norm_planes)
        
    def Pre_operations(self,image):
        blurr_image = cv2.GaussianBlur(image,(5,5),cv2.BORDER_DEFAULT)
        #Objective 2.a
        grey_image = cv2.cvtColor(blurr_image,cv2.COLOR_RGB2GRAY)
        self.image_array = grey_image.tolist()
        self.thresh_value = self.calculate_thresh(self.image_array)
        #Objective 2.c
        ret, thresholded = cv2.threshold(grey_image,self.thresh_value,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        thresholded = cv2.bitwise_not(thresholded)
        contour,hier = cv2.findContours(thresholded,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contour:
            cv2.drawContours(thresholded,[cnt],0,255,24)
        thresholded = cv2.bitwise_not(thresholded)
        thresholded = self.noise_removal(thresholded,30)
        thresholded = cv2.bitwise_not(thresholded)
        self.img = thresholded
        plt.imshow(self.img, cmap = "Greys_r")
        plt.show()
        return thresholded
    
    #Objective 2.g 
    def crop_top_image(self,image_array_input):
        image_array = image_array_input
        empty_space_count = 0
        length = len(image_array)
        for x in range(length):#FOR EACH ARRAY WITHIN THE 2D ARRAY
            if min(image_array[x]) == 255: #IF ALL ELEMENTS = 255, ADD 1 TO EMPTY SPACE COUNT
                empty_space_count += 1
            else:
                break #IF 1 ELEMENT WAS FOUND TO NOT BE 255 THEN MOVE ONTO THE NEXT ARRAY
        print("Top: ",empty_space_count)
        for y in range(int(empty_space_count * (3/4))):#RESERVE TO PIXELS TO NOT BE DELETED
            image_array.remove(image_array[0]) #FOR THE NUMBER OF COUNTS, REMOVE THE WHITE SPACES
        return image_array
    
    def crop_bottom_image(self,image_array_input): #SIMILAR PRINCIPLE AS CROP_TOP_IMAGE() FUNCTION
        image_array = image_array_input
        empty_space_count = 0
        for x in range ((len(image_array)-1),-1,-1): #ITERATE IN REVERSE
            if min(image_array[x]) == 255:
                empty_space_count += 1
            else:
                break
        print("Bottom: ",empty_space_count)
        for y in range(int(empty_space_count * (3/4))):
            del image_array[-1]
        return image_array

    #Objective 2.g
    def crop_whole_image(self,image_array_input):
        image_array = image_array_input
        image_array = self.crop_top_image(image_array)
        image_array = self.crop_bottom_image(image_array)#CROP TOP AND BOTTOM
        rotate_image = np.rot90(image_array,3) #ROTATE BY 270 DEGREES, EASIER TO CROP LEFT/RIGHT
        image_array = rotate_image.tolist() #CONVERT NUMPY ARRAY TO LIST
        image_array = self.crop_top_image(image_array)
        image_array = self.crop_bottom_image(image_array) #CROP LEFT AND RIGHT
        fully_cropped_image = np.rot90(image_array)#ROTATE IMAGE BACK TO ORIGINAL
        return np.asarray(fully_cropped_image, dtype = np.float32)
        #CONVERT LIST BACK TO NUMPY ARRAY IN ORDER TO BE DISPLAYED BY MATPLOTLIB

    #Objective 2.f
    def find_contour(self,image):
        cv2.imwrite("tmp.png",image)
        image = cv2.imread("tmp.png")
        image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        ret,thresh = cv2.threshold(image,self.thresh_value,255,cv2.THRESH_BINARY)
        contours, hierachy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        for x in range(1,len(contours)):
            cnt = contours[x]
            cv2.drawContours(thresh, [cnt], 0, (0,0,0),3)
        os.remove("tmp.png")
        return thresh

    #Objective 2.b
    def image_resize(self, image,SIZE):
        resize_img = cv2.resize(image,(SIZE,SIZE))
        ret,final_image = cv2.threshold(resize_img,self.thresh_value,255,cv2.THRESH_BINARY)
        return final_image

    #Objective 2.c
    def calculate_thresh(self,image_array): 
        mean_values = []
        for x in range(len(image_array)):
            mean_values.append(self.calculate_mean(image_array[x]))
        return self.calculate_mean(mean_values)
        
    def calculate_mean(self,list_value):
        total = 0
        for element in (list_value):
            total += element
        mean = round(total / len(list_value))
        return mean

    #Objective 2.e
    def find_ROI(self,image,DATADIR):
        #https://cvisiondemy.com/extract-roi-from-image-with-python-and-opencv/
        '''image = np.reshape(image,(np.shape(image)[0],np.shape(image)[1],1))'''
        ret, thresh = cv2.threshold(image, self.thresh_value, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((5,5),np.uint8)
        img_dilation = cv2.dilate(thresh, kernel, iterations=1)
        contours, hierachy = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # sort contours
        sorted_contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])
        
        for i, ctr in enumerate(sorted_contours):
            # Get bounding box
            x, y, w, h = cv2.boundingRect(ctr)

            # Getting ROI
            roi = image[y:y + h, x:x + w]
            cv2.rectangle(image, (x, y), (x + w, y + h), (255,255,255), 2)
            if w > 20 and h > 30:
                line_paper = False
                if line_paper:
                    image_array = np.asarray(roi)
                    cropped = self.crop_whole_image(image_array)
                    height,width = np.shape(cropped)
                    dimension = [width,height]
                    if np.max(dimension) > np.min(dimension) * 3:
                        print(dimension,"discard")
                    else:
                        save_dir = os.path.join(DATADIR, 'ROI' + str(i) + "." + 'png')
                        cv2.imwrite(save_dir, roi)
                else:
                    save_dir = os.path.join(DATADIR, 'ROI' + str(i) + "." + 'png')
                    cv2.imwrite(save_dir, roi)

    #Objective 2.d
    def noise_removal(self,image,kernel = 3):
        ret,thresh = cv2.threshold(image,self.thresh_value,255,cv2.THRESH_BINARY_INV)
        kernel = np.ones((kernel,kernel),np.uint8)
        opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening,cv2.MORPH_CLOSE, kernel)
        final = closing
        plt.imshow(final)
        plt.show()
        return final

    def padding(self,image,size):
        #https://jdhao.github.io/2017/11/06/resize-image-to-square-with-padding/
        WHITE = [255,255,255]
        small_pad = cv2.copyMakeBorder(image, 30, 30, 30, 30, cv2.BORDER_CONSTANT,value=WHITE)
        shape = [np.shape(small_pad)[0],np.shape(small_pad)[1]]
        factor = float(size / max(shape))
        enlargement = []
        for element in shape:
            enlargement.append(int(element * factor))
        small_pad = cv2.resize(small_pad,(enlargement[1],enlargement[0]))
        width_change = (size - enlargement[1]) // 2
        height_change = (size - enlargement[0]) // 2
        full_pad = cv2.copyMakeBorder(small_pad, height_change, height_change, width_change, width_change, cv2.BORDER_CONSTANT,value=WHITE)
        return full_pad

    def preprocess_img(self,DATADIR):
        #Do padding first, find contour and after resizing, do cropping
        padded_img = self.padding(self.img,300)
        found_contour = self.find_contour(padded_img)
        self.image_array = found_contour.tolist()
        cropped = self.crop_whole_image(self.image_array)
        noise_remove = self.noise_removal(cropped,5)
        final_image = self.image_resize(noise_remove,28)
        cv2.imwrite(os.path.join(DATADIR,'Final_image{number}.png'.format(number = self.count)),final_image)
        self.count += 1

    def show_images(self):
        f,axarr = plt.subplots(3,3)
        axarr[0,0].imshow(self.image_datas[0][0],cmap = "Greys_r")
        axarr[0,0].set_title(self.image_datas[0][1])
        axarr[0,1].imshow(self.image_datas[1][0],cmap = "Greys_r")
        axarr[0,1].set_title(self.image_datas[1][1])
        plt.show()

    def reset(self):
        self.img = None
        self.image_array = []
        self.thresh_value = 0
        self.image_datas = []
