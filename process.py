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
path = "/home/katherinee/Desktop/Job/Web_Reconig/"


def TakeImages(path, Id, name, department, position, username, password, email, phone, address, city):
    cam = cv2.VideoCapture(0)
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    sampleNum = 0
    while (True):
        print("Run")
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # incrementing sample number
            sampleNum = sampleNum+1
            # saving the captured face in the dataset folder TrainingImage
            os.chdir(path + "TrainingImage")
            cv2.imwrite(f"{str(Id)}_{str(sampleNum)}.jpg", img[y:y+h, x:x+w])
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
    db_user.insert_user_info(
        Id, name, department, position, username, password, email, phone, address, city)


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
        print(imagePath)
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


def Attendence():
    win = Tk()
    Id_attendance = 0
    change_or_inset = None
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(f"{path}TrainingImageLabel/Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = db_user.get_all_user()
    # col_names =  ['id', 'name', 'department', 'position', 'username', 'password', 'email',
    #   'phone', 'address', 'city']
    df = pd.DataFrame(df)
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['id', 'name', 'department', 'position', 'date',
                 'timecheckin', 'dayofweek', "timecheckout", "minuteslate", "worknumber"]
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
            if (conf < 50):
                user_info = db_user.get_user_info(Id)
                tt = user_info["name"] + "-" + user_info["position"]

                
                today = datetime.today()
                date = today.strftime('%Y-%m-%d')
                dayofweek = today.strftime('%A')
                minuteslate = 10
                worknumber = 1
                check_attendance = db_attendance.check_attendance(
                    date, user_info["name"])
                if check_attendance == None:
                    change_or_inset = "insert"
                    Id_attendance = np.random.randint(100000000, 999999999)
                    timecheckin = today.strftime('%H:%M:%S')
                    timecheckout = ""
                    Hour, Minute, Second = timecheckin.split(":")
                    if Hour >= '08' and Minute >= '00' and Second >= '00':
                        minuteslate = (int(Hour) - 8) * 60 + int(Minute)
                        if minuteslate > 120:
                            worknumber = 0
                        elif minuteslate > 60:
                            worknumber = 0.5

                else:
                    Id_attendance = check_attendance['id']
                    
                    timecheckout = today.strftime('%H:%M:%S')
                    timecheckin = check_attendance["timecheckin"]
                    timecheckin = str(timecheckin)
                    Hour, Minute, Second = timecheckout.split(":")
                    Hour_1, Minute_1, Second_1 = timecheckin.split(":")
                    if (int(Hour_1) == int(Hour)):
                        if  (int(Minute) - int(Minute_1)) >= 10:
                            change_or_inset = "update"
                    elif (int(Hour) > int(Hour_1)):
                        change_or_inset = "update"

                attendance.loc[len(attendance)] = [Id_attendance, user_info["name"], user_info["department"],
                                                   user_info["position"], date, timecheckin, dayofweek, timecheckout, minuteslate, worknumber]
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
    attendance = attendance.to_dict('records')
    attendance = attendance[-1]
    if change_or_inset == "insert":
        db_attendance.insert_user_attendance(attendance["id"], attendance["name"], attendance["department"], attendance["position"], attendance["date"],
                                        attendance["timecheckin"], attendance["dayofweek"], attendance["timecheckout"], attendance["minuteslate"], attendance["worknumber"])
    elif change_or_inset == "update":
        db_attendance.update_attendance(int(attendance["id"]), attendance["name"], attendance["department"], attendance["position"], str(attendance["date"]),
                                        str(attendance["timecheckin"]), attendance["dayofweek"], str(attendance["timecheckout"]), attendance["minuteslate"], attendance["worknumber"])
