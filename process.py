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
path = "C:/Users/chauk/OneDrive/Tài liệu/Code/Outsource/Python/Attendence/"


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
    # recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    recognizer = cv2.face_LBPHFaceRecognizer.create()
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


def Attendence(choose_class, choose_dayofweek, choose_time, choose_time_end):
    win = Tk()
    tt = ""
    minuteslate = 0
    check_attendance = None
    reason = ''
    Id_attendance = np.random.randint(100000000, 999999999)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(f"{path}TrainingImageLabel/Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = db_user.get_all_user()
    # col_names =  ['id', 'name', 'major', 'faculty', 'user_role', 'username', 'password', 'email',
    #   'phone', 'address', 'city']
    df = pd.DataFrame(df)
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['id', 'name', 'class_name', 'major', 'faculty',
                 'user_role', 'date', 'dayofwwek', 'minuteslate', "reason"]
    attendance = pd.DataFrame(columns=col_names)
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        image = Image.fromarray(gray)
        image = ImageTk.PhotoImage(image, master=win)

        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            print(Id)
            if (conf < 50):
                user_info = db_user.get_user_by_id(Id)
                if user_info:

                    tt = user_info["name"] + "-" + user_info["user_role"]
                    unidecode.unidecode(user_info["user_role"])

                    today = datetime.today()
                    date = today.strftime('%Y-%m-%d')
                    hour = today.strftime('%H:%M:%S')

                    minute = int(hour[3:5])
                    hour = int(hour[0:2])

                    # convert choose_time and choose_time_end to int to compare
                    choose_time_hour = int(choose_time[0:2])
                    choose_time_minute = int(choose_time[3:5])
                    choose_time_end_hour = int(choose_time_end[0:2])

                    check_attendance = db_attendance.check_user_attendance(
                        date, user_info["name"], choose_class, choose_dayofweek)

                    if check_attendance == False:
                        if hour == choose_time_hour:
                            if (minute - choose_time_minute) <= 15:
                                minuteslate = 0
                            else:
                                minuteslate = minute - choose_time_minute
                        elif hour > choose_time_hour and hour <= choose_time_end_hour:
                            minuteslate = (choose_time_hour - hour)*60 + minute

                        elif hour > choose_time_end_hour:
                            minuteslate = 100000
                            reason = "Muộn"

                        attendance.loc[len(attendance)] = [Id_attendance, user_info["name"], choose_class, user_info["major"],
                                                           user_info["faculty"], user_info["user_role"], date, choose_dayofweek, minuteslate, reason]

            else:
                Id = 'Unknown'
                tt = str(Id)
            if (conf > 75):
                noOfFile = len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite(f"{path}ImagesUnknown/Image" +
                            str(noOfFile) + ".jpg", im[y:y+h, x:x+w])
            cv2.putText(im, str(tt), (x, y+h), font, 1, (255, 255, 255), 2)
        attendance = attendance.drop_duplicates(subset=['name'], keep='first')
        cv2.imshow('im', im)
        if (cv2.waitKey(1) == ord('q')):
            break

    cam.release()
    cv2.destroyAllWindows()
    if check_attendance == False:
        attendance = attendance.to_dict('records')
        attendance = attendance[-1]
        db_attendance.insert_user_attendance(db_attendance.Attendance(attendance['id'], attendance['name'], attendance['class_name'], attendance[
                                             'major'], attendance['faculty'], attendance['date'], attendance['dayofwwek'], attendance['minuteslate'], attendance['reason']))
        st.success("Điểm danh thành cônh")
        st.balloons()
    elif check_attendance == "Bạn đã điểm danh rồi":
        st.error("Bạn đã điểm danh rồi")
    elif check_attendance == "Không có lớp hôm nay":
        st.error("Không có lớp hôm nay")
