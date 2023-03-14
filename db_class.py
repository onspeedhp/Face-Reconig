import mysql.connector
import numpy as np

password_db = "0931588846hP"

class Class:
    def __init__(self, id, class_name, major, faculty, time, time_end, dayofweek, students, teacher):
        self.id = id
        self.class_name = class_name
        self.major = major
        self.faculty = faculty
        self.time = time
        self.time_end = time_end
        self.dayofweek = dayofweek
        self.students = students
        self.teacher = teacher
    def to_dict(self):
        return {
            'id': self.id,
            'class_name': self.class_name,
            'major': self.major,
            'faculty': self.faculty,
            'time': self.time,
            'time_end': self.time_end,
            'dayofweek': self.dayofweek, 
            'students': self.students,
            'teacher': self.teacher
        }


def insert_new_class(Major):
    id = np.random.randint(100000000, 999999999)

    try:
        cnx = mysql.connector.connect(user='root', password=password_db,
                                      host='localhost',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        query = f"INSERT INTO major (id, class, major, faculty, time, time_end, dayofweek, students, teacher) VALUES ({Major.id}, '{Major.class_name}', '{Major.major}', '{Major.faculty}', '{Major.time}', '{Major.time_end}', '{Major.dayofweek}', '{Major.students}', '{Major.teacher}')"
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        cnx.close()
    except ValueError:
        print("Major info is not valid")

def update_class_info(Major):
    try:
        cnx = mysql.connector.connect(user='root', password=password_db,
                                      host='localhost',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        query = f"UPDATE major set class = '{Major.class_name}', major = '{Major.major}', faculty = '{Major.faculty}', time = '{Major.time}', time_end = '{Major.time_end}', dayofweek = '{Major.dayofweek}', students = '{Major.students}', teacher = '{Major.teacher}' WHERE id = '{Major.id}';"
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        cnx.close()
    except ValueError:
        print("Major info is not valid")

def get_all_class():
    all_major = []
    try:
        cnx = mysql.connector.connect(user='root', password=password_db,
                                      host='localhost',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        query = "SELECT * FROM major"
        cursor.execute(query)
        for (id, class_name, major, faculty, time, time_end, dayofweek, students, teacher) in cursor:
            all_major.append(Class(id, class_name, major, faculty,
                             time, time_end, dayofweek, students, teacher).to_dict())
        cursor.close()
        cnx.close()
    except ValueError:
        print("Major info is not valid")

    return all_major


def get_class_by_major(major):
    data = get_all_class()
    result = []
    for i in data:
        if i['major'] == major:
            result.append(i)
    return result


def get_major_by_faculty(faculty):
    data = get_all_class()
    result = []
    for i in data:
        if i['faculty'] == faculty:
            if i['major'] not in result:
                result.append(i['major'])
    return result


def get_unique_faculty():
    data = get_all_class()
    result = []
    for i in data:
        if i['faculty'] not in result:
            result.append(i['faculty'])
    return result

def get_class_by_teacher(teacher):
    data = get_all_class()
    result = []
    for i in data:
        if i['teacher'] == str(teacher):
            result.append(i["class_name"])
    return result

def get_class_by_class_name(class_name):
    data = get_all_class()
    result = []
    for i in data:
        if i['class_name'] == class_name:
            result.append(i)
    return result[-1]


def delete_class_by_id(id):
    try:
        cnx = mysql.connector.connect(user='root', password=password_db,
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)

        query = f"DELETE FROM major WHERE id = '{id}';"
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        cnx.close()
    except ValueError:
        return

# insert_new_class(Class(123456789, 'Statistic', 'Computer Science', 'IT', '09:00:00', 'Tuesday', '', ''))
