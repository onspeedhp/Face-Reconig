from db_class import *
import cv2
from tkinter import *
import csv
import os
import numpy as np
from PIL import Image
import pandas as pd
import numpy as np
from PIL import Image, ImageTk
from datetime import datetime
from datetime import date
from db_user import *
from db_attendence import *
import streamlit as st
import unidecode
import calendar

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
    insert_user_info(student)


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

    dt = datetime.now()

    my_date = date.today()
    x = calendar.day_name[my_date.weekday()]

    time = dt.strftime("%H:%M:%S")
    date_attendence = dt.strftime("%d/%m/%Y")
    hour_now, minute_now, second_now = time.split(":")

    hour_class_begin, minute_class_begin, second_class_begin = class_info["time"].split(
        ":")

    hour_class_end, minute_class_end, second_class_end = class_info["time_end"].split(
        ":")

    # if in time can take attendence else not
    if int(hour_now) >= int(hour_class_begin) and int(hour_now) <= int(hour_class_end):
        if int(minute_now) >= int(minute_class_begin) and int(minute_now) <= int(minute_class_end):
            tt = "Đang diễn ra"
        else:
            tt = "Chưa đến giờ"
    else:
        tt = "Chưa đến giờ"

    if tt == "Đang diễn ra":

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
                student = get_user_by_id(Id)
                if (conf < 50):
                    if student:
                        tt = student["name"] + "_" + str(student["id"])
                        student_attendence.append(student["id"])
                else:
                    Id = 'Unknown'
                    tt = str(Id)
                if (conf > 75):
                    tt = str(Id)
                cv2.putText(im, str(tt), (x, y+h), font, 1, (255, 255, 255), 2)
            cv2.imshow('im', im)
            if (cv2.waitKey(1) == ord('q')):
                break

        cam.release()
        cv2.destroyAllWindows()

        student_attendence = list(dict.fromkeys(student_attendence))
        students = ""
        for i in range (len(student_attendence)):
            students += str(student_attendence[i]) + ","

        id = np.random.randint(100000000, 999999999)
        insert_user_attendence(attendence(
            id, class_info["class_name"], class_info["major"], class_info["faculty"], time, date_attendence, class_info["dayofweek"], students, class_info["teacher"]))
    else:
        st.text("Chưa đến giờ")


def dayofweek_to_thu(x):
    if x == "Monday":
        x = "Thứ hai"
    elif x == "Tuesday":
        x = "Thứ ba"
    elif x == "Wednesday":
        x = "Thứ tư"
    elif x == "Thursday":
        x = "Thứ năm"
    elif x == "Friday":
        x = "Thứ sáu"
    elif x == "Saturday":
        x = "Thứ bảy"
    elif x == "Sunday":
        x = "Chủ nhật"
    return x

# test
# id = np.random.randint(100000000, 999999999)
# user = User(id, "Trung", "Việt Nhật", "Công nghệ thông tin",
#                               "Học sinh", "4", "1", "", "", "", "")

# TakeImages(path, user)

# class_info = get_class_by_class_name("Quản trị học")

# Attendence(class_info)


def thongke(class_info):
    class_attendence = get_attendence_by_class_name(class_info["class_name"])
    dates = []
    for i in range(len(class_attendence)):
        dates.append(class_attendence[i]["date"])

    choose_date = st.selectbox("Chọn ngày", dates)

    if choose_date:
        class_info_attendence = get_attendence_by_class_name_and_date(
            class_info["class_name"], choose_date)
        
        df = attendence_to_thongke(class_info_attendence, class_info)
        
        return df

    # student_id_list = class_info["students"].split(",")
    # student_id_list.pop(-1)

    # col_attendence = ["STT", "Mã số sinh viên", "Họ và tên",
    #                   "Ngày tháng", "Thời gian", "Trạng thái"]

    # df = pd.DataFrame(columns=col_attendence)

    # for i in range(len(student_id_list)):
    #     print(student_id_list[i])
    #     student = get_user_by_id(int(student_id_list[i]))
    #     df.loc[i] = [i+1, student["id"], student["name"], "--/--/--", "--:--:--", "Vắng"]

    # # save to csv
    # time = datetime.now().strftime("%d_%m_%Y")

    # student_attendence = []

    # for i in range(len(student_attendence)):
    #     df.loc[df["Mã số sinh viên"] == student_attendence[i],
    #            "Trạng thái"] = "Có mặt"

    #     df.loc[df["Mã số sinh viên"] == student_attendence[i],
    #            "Ngày tháng"] = datetime.now().strftime("%d/%m/%Y")

    #     df.loc[df["Mã số sinh viên"] == student_attendence[i],
    #            "Thời gian"] = datetime.now().strftime("%H:%M:%S")

    # save to csv
    # time = datetime.now().strftime("%d_%m_%Y")


def attendence_to_thongke(class_info_attendence, class_info):

    student_id_list = class_info["students"].split(",")
    student_id_list.pop(-1)

    student_attendence = class_info_attendence["students"].split(",")
    student_attendence.pop(-1)

    col_attendence = ["STT", "Mã số sinh viên", "Họ và tên",
                        "Ngày tháng", "Thời gian", "Trạng thái"]
    
    df = pd.DataFrame(columns=col_attendence)

    for i in range(len(student_id_list)):
        student = get_user_by_id(int(student_id_list[i]))
        df.loc[i] = [i+1, student["id"], student["name"], "--/--/--", "--:--:--", "Vắng"]
        print(type(student["id"]))

    for i in range(len(student_attendence)):
        df.loc[df["Mã số sinh viên"] == int(student_attendence[i]),
                "Trạng thái"] = "Có mặt"

        df.loc[df["Mã số sinh viên"] == int(student_attendence[i]),
                "Ngày tháng"] = class_info_attendence["date"]

        df.loc[df["Mã số sinh viên"] == int(student_attendence[i]),
                "Thời gian"] = class_info_attendence["time"]
        
    return df
