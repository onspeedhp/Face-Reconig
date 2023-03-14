from db_class import *
import cv2
from tkinter import *
import csv
import os
import numpy as np
from PIL import Image
import db_user as db_user
import pandas as pd
import numpy as np
from PIL import Image, ImageTk
from datetime import datetime
import db_user as db_user
import db_attendance as db_attendance
import streamlit as st
import unidecode

path = "C:/Users/chauk/OneDrive/Máy tính/New folder/Web-Reconig/"


def TakeImages(path, student):
    cam = cv2.VideoCapture(0)
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    sampleNum = 0
    while (True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # incrementing sample number
            sampleNum = sampleNum+1
            # saving the captured face in the dataset folder TrainingImage
            os.chdir(path + "TrainingImage")
            cv2.imwrite(f"{str(student.id)}_{str(sampleNum)}.jpg",
                        img[y:y+h, x:x+w])
            # display the frame
            cv2.imshow('frame', img)
        # wait for 100 miliseconds
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        # break if the sample number is morethan 100
        elif sampleNum > 50:
            break
    cam.release()
    cv2.destroyAllWindows()
    TrainImages()
    db_user.insert_user_info(student)


def TrainImages():
    # recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer = cv2.face.LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, Id = getImagesAndLabels(f"{path}TrainingImage/")
    recognizer.train(faces, np.array(Id))
    recognizer.save(f"{path}TrainingImageLabel/Trainner.yml")


def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # print(imagePaths)

    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        Id = int(os.path.split(imagePath)[-1].split("_")[0])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids


def Attendence(class_info):
    win = Tk()
    tt = ""

    student_id_list = class_info["students"].split(",")
    student_id_list.pop(-1)
    
    col_attendence = ["STT", "Mã số sinh viên", "Họ và tên",
                      "Ngày tháng", "Thời gian", "Trạng thái"]

    df = pd.DataFrame(columns=col_attendence)

    for i in range(len(student_id_list)):
        print(student_id_list[i])
        student = db_user.get_user_by_id(int(student_id_list[i]))
        df.loc[i] = [i+1, student["id"], student["name"], "--/--/--", "--:--:--", "Vắng"]

    # save to csv
    time = datetime.now().strftime("%d_%m_%Y")
    df.to_csv(f"{path}Attendance/{class_info['id']}_{time}.csv", index=False)

    student_attendence = []

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(f"{path}TrainingImageLabel/Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        image = Image.fromarray(gray)
        image = ImageTk.PhotoImage(image, master=win)

        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            student = db_user.get_user_by_id(Id)
            if (conf < 50):
                if student:
                    print(student["id"])
                    tt = student["name"] + "_" + str(student["id"])
                    student_attendence.append(student["id"])
            else:
                Id = 'Unknown'
                tt = str(Id)
            if (conf > 75):
                # noOfFile = len(os.listdir("ImagesUnknown"))+1
                # cv2.imwrite(f"{path}ImagesUnknown/Image" +
                #             str(noOfFile) + ".jpg", im[y:y+h, x:x+w])
                tt = str(Id)
            cv2.putText(im, str(tt), (x, y+h), font, 1, (255, 255, 255), 2)
        cv2.imshow('im', im)
        if (cv2.waitKey(1) == ord('q')):
            break

    cam.release()
    cv2.destroyAllWindows()

    student_attendence = list(dict.fromkeys(student_attendence))

    for i in range(len(student_attendence)):
        df.loc[df["Mã số sinh viên"] == student_attendence[i], 
               "Trạng thái"] = "Có mặt"

        df.loc[df["Mã số sinh viên"] == student_attendence[i], 
               "Ngày tháng"] = datetime.now().strftime("%d/%m/%Y")
        
        df.loc[df["Mã số sinh viên"] == student_attendence[i], 
               "Thời gian"] = datetime.now().strftime("%H:%M:%S")
        
    # save to csv
    time = datetime.now().strftime("%d_%m_%Y")
    df.to_csv(f"{path}Attendance/{class_info['id']}_{time}.csv", index=False)
    
# test
# id = np.random.randint(100000000, 999999999)
# user = db_user.User(id, "Trung", "Việt Nhật", "Công nghệ thông tin",
#                               "Học sinh", "4", "1", "", "", "", "")

# TakeImages(path, user)

# class_info = get_class_by_class_name("Quản trị học")

# Attendence(class_info)
