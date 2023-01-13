import cv2
import numpy as np
import face_recognition as fr
import tkinter as tk
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = BASE_DIR + '\ImageList'
images = []
classNames = []
myList = os.listdir(path)
print(myList)

for cls in myList:
    curImg = cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0])
print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList
        
encodeListKnown = findEncodings(images)
print('Encoding Complete')
cap = cv2.VideoCapture(1)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS =cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    faceCurFrame = fr.face_locations(imgS)
    encodeCurFrame =fr.face_encodings(imgS, faceCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = fr.compare_faces(encodeListKnown, encodeFace)
        faceDis = fr.face_distance(encodeListKnown, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img,(x1,y1), (x2,y2), (0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0, 255, 0), cv2.FILLED)
            cv2.putText(img, name,(x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0),2)
    cv2.imshow('webcam',img)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break
    cv2.destroyAllWindows