import cv2
# import numpy as np
# import face_recognition as fr
# import tkinter.filedialog as FileDialog
import customtkinter as ct
from PIL import Image, ImageTk
import os

ct.set_appearance_mode("system")
ct.set_default_color_theme("dark-blue")

class App(ct.CTk):
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        super().__init__()

        self.cap = cv2.VideoCapture(1) # Change as needed

        self.WIDTH = self.winfo_screenwidth()
        self.HEIGHT = self.winfo_screenheight()

        self.title("Face Recognition App")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(False, False)
        self.state("zoomed")
        self.img_holder = ct.CTkLabel(master=self, corner_radius=0, width=625, height=500, text="Loading camera...")
        self.img_holder.grid(column=0, row=0, sticky="NSEW")

        # Frame Right
        self.frame_right = ct.CTkFrame(master=self, fg_color="yellow", corner_radius=0, width=75, height=500)
        self.frame_right.grid(column=1, row=0, sticky="NSEW")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.img_holder.columnconfigure(0, weight=1)
        self.frame_right.columnconfigure(0, weight=1)

        self.prepCamera()
        self.openCamera()

    def prepCamera(self):
        self.update_idletasks()
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.img_holder.winfo_width())
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.img_holder.winfo_height())
        self.cap.set(cv2.CAP_PROP_FPS, 25)

    def openCamera(self):
        _, frame = self.cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        prevImg = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=prevImg)
        self.img_holder.imgtk=imgtk
        self.img_holder.configure(image=imgtk)
        self.img_holder.after(20, self.openCamera)
        

if __name__ == "__main__":
    app = App()
    app.mainloop()



# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# path = BASE_DIR + '\ImageList'
# images = []
# classNames = []
# myList = os.listdir(path)
# print(myList)

# for cls in myList:
#     curImg = cv2.imread(f'{path}/{cls}')
#     images.append(curImg)
#     classNames.append(os.path.splitext(cls)[0])
# print(classNames)

# def findEncodings(images):
#     encodeList = []
#     for img in images:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode = fr.face_encodings(img)[0]
#         encodeList.append(encode)

#     return encodeList
        
# encodeListKnown = findEncodings(images)
# print('Encoding Complete')
# cap = cv2.VideoCapture(1)

# while True:
#     success, img = cap.read()
#     imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
#     imgS =cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
#     faceCurFrame = fr.face_locations(imgS)
#     encodeCurFrame =fr.face_encodings(imgS, faceCurFrame)

#     for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
#         matches = fr.compare_faces(encodeListKnown, encodeFace)
#         faceDis = fr.face_distance(encodeListKnown, encodeFace)
#         print(faceDis)
#         matchIndex = np.argmin(faceDis)

#         if matches[matchIndex]:
#             name = classNames[matchIndex].upper()
#             print(name)
#             y1, x2, y2, x1 = faceLoc
#             y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
#             cv2.rectangle(img,(x1,y1), (x2,y2), (0,255,0),2)
#             cv2.rectangle(img,(x1,y2-35),(x2,y2),(0, 255, 0), cv2.FILLED)
#             cv2.putText(img, name,(x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0),2)
#     cv2.imshow('webcam',img)
#     if cv2.waitKey(1) & 0XFF == ord('q'):
#         break
#     cv2.destroyAllWindows