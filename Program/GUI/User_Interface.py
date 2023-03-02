from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter import messagebox

class GUI(Frame):
    def __init__(self, window_pos, master=None):
        Frame.__init__(self, master)
        self.operation = ""
        self.master = master
        self.master.filepath = ""
        self.window_pos = window_pos
        self.init_window()

    def init_window(self):
        self.master.title("Main") #Name of the frame
        
        self.pack(fill=BOTH, expand=1) #Widget fill empty space
        #Objective 1.a
        input_button = Button(self,text = "Open Image File",width = 28,
                              height = 4, bg = "#379683", fg ="Black",
                              command = self.Open_Image) #Open_Image button
        instruction_button =Button(self,text = "Instructions",width = 28,
                                   height = 4,bg = "#5CDB95",fg ="Black",
                                   command = self.display_instruction)
                                    #Instructions Button
        exit_button = Button(self,text = "Exit", width = 28, height = 4,
                             bg = "#AFD275",fg ="Black",
                             command = self.quitting)#Objective 1.h
        input_button.place(x=0,y=0)
        instruction_button.place(x=0,y=70)
        exit_button.place(x=0,y=140)
        self.master.protocol("WM_DELETE_WINDOW",self.quitting)
        #Placing of buttons with specified coordinates and place them on frame

        #Set coordinates of buttons and place them on the frame

    def quitting(self):
        #Display message asking whether user would like to quit or not
        if messagebox.askokcancel("End Program","Do you want to exit the program?"):
            self.master.destroy()

    def format_window(self,window,name):
        #Format window so that they're displayed at the centre of the screen and aren't resizable
        window.geometry('250x210')
        window.geometry("+{}+{}".format(self.window_pos[0],self.window_pos[1])) 
        window.resizable(False,False)
        window.title(name)
        window.attributes('-topmost','true')
        self.master.withdraw() #Hide main Frame
        window.protocol("WM_DELETE_WINDOW",lambda:[window.destroy(),self.master.deiconify()])
        #Redisplay main window if the window is closed
    def Open_Image(self):
        #Objective 1.b
        extensionsToCheck = [".png",".jpg",".jpeg",".tiff",".gif",".bmp",".bat"]
        self.master.withdraw() #Hides main window
        #File extensions of image files, may need to add more
        file = askopenfilename(filetypes=(("All", "*.*"),
                                          ("PNG", "*.png"),
                                          ("JPG", "*.jpg;*.jpeg"),
                                          ("TIFF", "*.tiff"),
                                          ("GIF", "*.gif"),
                                          ("BMP", "*.bmp"),
                                          ("BAT", "*.bat")))
        #Ask user to input file in order to obtain file directory, may need to add more
        if file.lower() == "":
            self.master.deiconify()
        elif not any(ext in file.lower() for ext in extensionsToCheck):
            #Objective 1.c
            #Ensures file inputted is an image file
            showerror(title = "Error",message = "Unknown filetype inputted")
            #Raise error, display error window
            label = Label(self,text = ("Please input an image file"))
            label.config(font=("Courier", 10)) 
            label.place(x=250,y=100)
            #Objective 1.f
            self.master.deiconify() #Redisplay main window
        else:
            self.master.filepath = file #File directory
            self.operation_option()

    def operation_option(self):
        #Objective 1.d
        window = Toplevel() #Creating a frame on top of the root frame
        self.format_window(window,'Operation')
        label = Label(window,text = ("Please select an option"),width = 40)
        label.config(font=("Courier", 10))
        label.pack()
        single_letter_button = Button(window,text = "Single Letter Prediction",
                                      width = 30,height = 5, bg = "#379683", fg ="Black",
                                      command = self.single_letter).pack()
        entire_text_button = Button(window,text = "Entire Text Prediction",
                                    width = 30,height = 5, bg = "#5CDB95",fg ="Black",
                                    command = self.entire_text).pack() #Buttons

    def single_letter(self):
        #Objective 1.e
        self.operation = ("Single")
        self.master.destroy()
        
    def entire_text(self):
        #Objective 1.e
        self.operation =("Entire")
        self.master.destroy()
        
    def display_instruction(self):
        #Objective 1.g
        window = Toplevel() #Create another frame
        self.format_window(window,'Instruction')
        label = Label(window,text = ("Instructions: \n1.Please input an image file \nusing the open image file button\n\n2.After inputting, please \nselect an appropriate mode\n\n3.Please ensure that text \nis legible for human and is \nwritten on plain sheet of paper\n\n4.Please be patient while \nwaiting for the prediction" ),width = 40)
        label.config(font=("Courier", 8))
        label.pack()
        return_menu_button = Button(window,text = "Back to main menu",
                                    width = 15, bg = "#AFD275", fg ="Black",
                                    command = lambda:[window.destroy(),self.master.deiconify()]).pack()
        #Destroy instruction window and re-display main Frame window

    def return_image_directory(self): #Return extracted image directory
        return self.master.filepath

    def return_operation_type(self):  #Return selected operation type
        return self.operation
