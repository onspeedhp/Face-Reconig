import mysql.connector
import datetime
from datetime import datetime
import streamlit as st

password_db = "0931588846hP"


class Attendance:
    def __init__(self, id, name, class_name, major, faculty, date, dayofweek, minuteslate, reason):
        self.id = id
        self.name = name
        self.class_name = class_name
        self.major = major
        self.faculty = faculty
        self.date = date
        self.dayofweek = dayofweek
        self.minuteslate = minuteslate
        self.reason = reason

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "class_name": self.class_name,
            "major": self.major,
            "faculty": self.faculty,
            "date": self.date,
            "dayofweek": self.dayofweek,
            "minuteslate": self.minuteslate,
            "reason": self.reason
        }


def insert_user_attendance(Attendance):
    try:
        cnx = mysql.connector.connect(user='root', password=password_db,
                                      host='localhost',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        query = f"INSERT INTO attendance (id, name, class_name, major, faculty, date, dayofweek, minuteslate, reason) VALUES ({Attendance.id}, '{Attendance.name}', '{Attendance.class_name}', '{Attendance.major}', '{Attendance.faculty}', '{Attendance.date}', '{Attendance.dayofweek}', '{Attendance.minuteslate}', '{Attendance.reason}')"
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        cnx.close()
    except ValueError:
        print("User info is not valid")


def get_all_user_attendance():
    df_all_attendance = []
    try:
        cnx = mysql.connector.connect(user='root', password=password_db,
                                      host='localhost',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        query = f"SELECT * FROM attendance"
        cursor.execute(query)
        for (id, name, class_name, major, faculty, date, dayofweek, minuteslate, reason) in cursor:
            df_all_attendance.append(Attendance(
                id, name, class_name, major, faculty, date, dayofweek, minuteslate, reason).to_dict())

    except ValueError:
        print("User info is not valid")
    return df_all_attendance


def check_user_attendance(date, name, choose_class, choose_dayofweek):
    data = get_all_user_attendance()
    today = datetime.today()
    date = today.strftime('%Y-%m-%d')
    dayofweek = today.strftime('%A')

    if dayofweek != choose_dayofweek:
        return "Không có lớp hôm nay"
    else:
        for i in range(len(data)):
            if data[i]['date'] == date and data[i]['name'] == name and data[i]['class_name'] == choose_class:
                return "Bạn đã điểm danh rồi"
        return False

# insert_user_attendance('1', 'John', 'IT', 'Manager', '2021-01-01', '08:00:00', 'Monday', '17:00:00', '0', '0')
