import mysql.connector
import datetime
from datetime import datetime
import streamlit as st

password_db = "0931588846hP"


class attendence:
    def __init__(self, id, class_name, major, faculty, time, date, dayofweek, students, teacher):
        self.id = id
        self.class_name = class_name
        self.major = major
        self.faculty = faculty
        self.time = time
        self.date = date
        self.dayofweek = dayofweek
        self.students = students
        self.teacher = teacher

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "major": self.major,
            "faculty": self.faculty,
            "time": self.time,
            "date": self.date,
            "dayofweek": self.dayofweek,
            "students": self.students,
            "reason": self.teacher
        }


def insert_user_attendence(attendence):
    print("Hehe")
    try:
        cnx = mysql.connector.connect(user='root', password=password_db,
                                      host='localhost',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        query = f"INSERT INTO attendence (id, class, major, faculty, time, date, dayofweek, students, teacher) VALUES ({attendence.id}, '{attendence.class_name}', '{attendence.major}', '{attendence.faculty}', '{attendence.time}', '{attendence.date}', '{attendence.dayofweek}', '{attendence.students}', '{attendence.teacher}')"
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        cnx.close()
    except ValueError:
        print("User info is not valid")

    st.balloons()


def get_all_attendence():
    df_all_attendence = []
    try:
        cnx = mysql.connector.connect(user='root', password=password_db,
                                      host='localhost',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        query = f"SELECT * FROM attendence"
        cursor.execute(query)
        for (id, class_name, major, faculty, time, date, dayofweek, students, teacher) in cursor:
            df_all_attendence.append(attendence(
                id, class_name, major, faculty, time, date, dayofweek, students, teacher).to_dict())

    except ValueError:
        print("User info is not valid")
    return df_all_attendence

def get_attendence_by_class_name(class_name):
    attendences = get_all_attendence()
    class_attendence = []
    for i in attendences:
        if i["class_name"] == class_name:
            class_attendence.append(i)
    return class_attendence

def get_attendence_by_class_name_and_date(class_name, date):
    attendences = get_all_attendence()
    for i in attendences:
        if i["class_name"] == class_name and i["date"] == date:
            return i