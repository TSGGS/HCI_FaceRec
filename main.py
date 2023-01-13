import cv2
import numpy as np
import face_recognition as fr
import tkinter.filedialog as FileDialog
import customtkinter as ct
from PIL import Image, ImageTk
import os

ct.set_appearance_mode("system")
ct.set_default_color_theme("dark-blue")

class App(ct.CTk):
    def __init__(self):
        super().__init__()

        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.path = self.BASE_DIR + '\ImageList'
        self.images = []
        self.classNames = []
        self.myList = os.listdir(self.path)
        print(self.myList)

        for cls in self.myList:
            curImg = cv2.imread(f'{self.path}/{cls}')
            self.images.append(curImg)
            self.classNames.append(os.path.splitext(cls)[0])
        print(self.classNames)

        self.encodeListKnown = self.findEncodings(self.images)
        print('Encoding Complete')

        # ==================================================================================
        self.WIDTH = self.winfo_screenwidth()
        self.HEIGHT = self.winfo_screenheight()

        self.title("Face Recognition App")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(False, False)
        self.state("zoomed")
        self.img_holder = ct.CTkLabel(master=self, corner_radius=0, width=625, height=500, text="Loading camera...", text_font=("Lucida", 20))
        self.img_holder.grid(column=0, row=0, sticky="NSEW")

        self.switch_cam_icon = ImageTk.PhotoImage(Image.open(self.BASE_DIR + "\img\camera-rev.png").resize((70,70)))
        self.capture_icon = ImageTk.PhotoImage(Image.open(self.BASE_DIR + "\img\camera.png").resize((70,70)))
        self.detect_icon = ImageTk.PhotoImage(Image.open(self.BASE_DIR + "\img\detect.png").resize((70,70)))

        # Frame Right
        self.frame_right = ct.CTkFrame(master=self, corner_radius=0, width=76, height=500)
        self.frame_right.grid(column=1, row=0, sticky="NSEW")

        self.change_cam = ct.CTkButton(master=self.frame_right, fg_color="white", hover_color="#aaaaaa", corner_radius=0, width=10, height=100, image=self.switch_cam_icon, command=self.switch_cam)
        self.change_cam.place(x=0, y=0)

        self.capture = ct.CTkButton(master=self.frame_right, fg_color="white", hover_color="#aaaaaa", corner_radius=0, width=10, height=100, image=self.capture_icon, command=self.capture)
        self.capture.place(anchor="w", x=0, y=372)

        self.detect = ct.CTkButton(master=self.frame_right, fg_color="white", hover_color="#aaaaaa", corner_radius=0, width=10, height=100, image=self.detect_icon, command=self.detect)
        self.detect.place(anchor="sw", x=0, y=744)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.img_holder.columnconfigure(0, weight=1)

        self.cam_index = self.loadCamera()
        self.prepCamera()
        self.openCamera()

    def findEncodings(self, images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = fr.face_encodings(img)[0]
            encodeList.append(encode)

        return encodeList

    def loadCamera(self):
        self.cam_list = os.environ['ALLUSERSPROFILE'] + "\WebcamCap.txt"
        try:
            f = open(self.cam_list, 'r')
            return int(f.readline())
        except:
            return 0


    def prepCamera(self):
        self.update_idletasks()
        self.cap = cv2.VideoCapture(self.cam_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.img_holder.winfo_width())
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.img_holder.winfo_height())
        self.cap.set(cv2.CAP_PROP_FPS, 25)

    def openCamera(self):
        global prevImg

        _, frame = self.cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        prevImg = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=prevImg)
        self.img_holder.imgtk=imgtk
        self.img_holder.configure(image=imgtk)
        self.img_holder.after(20, self.openCamera)

    def switch_cam(self, event=0, nextCam=-1):
        if nextCam == -1:
            self.cam_index += 1
        else:
            self.cam_index = nextCam
        del(self.cap)
        self.prepCamera()

        success, frame = self.cap.read()
        if not success:
            self.cam_index = 0
            del(self.cap)
            self.prepCamera()

        # Add existing list of previously accessed camera to a file
        f = open(self.cam_list, "w")
        f.write(str(self.cam_index))
        f.close()

    def capture(self):
        global prevImg

        file = FileDialog.asksaveasfile(initialdir=f"{self.BASE_DIR}\ImageList", defaultextension=".png", filetypes=[("Portable Network Graphics", ".png"), ("JPEG", [".jpg", ".jpeg"]), ("All files", ".*")], title="Save Image")

        if file is not None:
            prevImg.save(file.name);

    def detect(self):
        while True:
            success, img = self.cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            faceCurFrame = fr.face_locations(imgS)
            encodeCurFrame =fr.face_encodings(imgS, faceCurFrame)

            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = fr.compare_faces(self.encodeListKnown, encodeFace)
                faceDis = fr.face_distance(self.encodeListKnown, encodeFace)
                print(faceDis)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = self.classNames[matchIndex].upper()
                    print(name)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                    cv2.rectangle(img,(x1,y1), (x2,y2), (0,255,0),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name,(x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0),2)
            cv2.imshow('webcam',img)
            if cv2.waitKey(1) & 0XFF == ord('q'):
                self.cap.release()
                cv2.destroyAllWindows()
                self.prepCamera()
                break

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
#     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
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