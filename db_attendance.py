import mysql.connector
import datetime
from datetime import datetime
def get_user_attendance(name):
    try:
        cnx = mysql.connector.connect(user='root', password='12345678hP.',
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)

        querry = f"SELECT * FROM attendance where name = '{name}'"
        cursor.execute(querry)
        for (id, name, department, position, date, timecheckin, dayofweek, timecheckout, minuteslate, worknumber) in cursor:
            print(id, name, department, position, date, timecheckin,
                  dayofweek, timecheckout, minuteslate, worknumber)

    except ValueError:
        print("Invalid name")


def insert_user_attendance(id, name, department, position, date, timecheckin, dayofweek, timecheckout, minuteslate, worknumber):
    try:
        cnx = mysql.connector.connect(user='root', password='12345678hP.',
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        querry = f"INSERT INTO attendance (id, name, department, position, date, timecheckin, dayofweek, timecheckout, minuteslate, worknumber) VALUES ('{id}', '{name}', '{department}', '{position}', '{date}', '{timecheckin}', '{dayofweek}', '{timecheckout}', '{minuteslate}', '{worknumber}')"
        cursor.execute(querry)
        cnx.commit()
        cursor.close()
        cnx.close()
    except ValueError:
        print("User info is not valid")


def get_all_user_attendance():
    df_all_attendance = []
    try:
        cnx = mysql.connector.connect(user='root', password='12345678hP.',
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        querry = f"SELECT * FROM attendance"
        cursor.execute(querry)
        for (id, name, department, position, date, timecheckin, dayofweek, timecheckout, minuteslate, worknumber) in cursor:
            user_attendance = {"id": id, "name": name, "department": department, "position": position, "date": date, "timecheckin": timecheckin,
                               "dayofweek": dayofweek, "timecheckout": timecheckout, "minuteslate": minuteslate, "worknumber": worknumber}
            df_all_attendance.append(user_attendance)
            
        return df_all_attendance
    except ValueError:
        pass


def calculate_work_number(name):
    try:
        cnx = mysql.connector.connect(user='root', password='12345678hP.',
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        querry = f"SELECT * FROM attendance where name = '{name}'"
        cursor.execute(querry)
        for (id, name, department, position, date, timecheckin, dayofweek, timecheckout, minuteslate, worknumber) in cursor:
            print(id, name, department, position, date, timecheckin,
                  dayofweek, timecheckout, minuteslate, worknumber)

    except ValueError:
        print("Invalid ID")


def calculate_minutes_late_in_month(name):
    try:
        cnx = mysql.connector.connect(user='root', password='12345678hP.',
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        querry = f"SELECT minuteslate FROM attendance where name = '{name}' and date between '2021-01-01' and '2023-01-31'"
        cursor.execute(querry)
        for (minuteslate) in cursor:
            print(minuteslate)
    except ValueError:
        pass


def check_attendance(date, name):
    user_attendance = None
    try:
        cnx = mysql.connector.connect(user='root', password='12345678hP.',
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        querry = f"SELECT * FROM attendance where date = '{date}' and name = '{name}'"
        cursor.execute(querry)
        for (id, name, department, position, date, timecheckin, dayofweek, timecheckout, minuteslate, worknumber) in cursor:
            user_attendance = {"id": id, "name": name, "department": department, "position": position, "date": date, "timecheckin": timecheckin,
                               "dayofweek": dayofweek, "timecheckout": timecheckout, "minuteslate": minuteslate, "worknumber": worknumber}
        return user_attendance
    except ValueError:
        return False


def update_attendance(id, name, department, position, date, timecheckin, dayofweek, timecheckout, minuteslate, worknumber):
    try:
        cnx = mysql.connector.connect(user='root', password='12345678hP.',
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        querry = f"UPDATE attendance SET timecheckout = '{timecheckout}' where id = '{id}'"
        cursor.execute(querry)
        cnx.commit()
        cursor.close()
        cnx.close()
    except ValueError:
        return False


# insert_user_attendance('1', 'John', 'IT', 'Manager', '2021-01-01', '08:00:00', 'Monday', '17:00:00', '0', '0')