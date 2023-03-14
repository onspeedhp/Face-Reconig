import mysql.connector
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import streamlit as st
import numpy as np

password_db = "0931588846hP"


class User:
    def __init__(self, id, name, major, faculty, user_role, username, password, email, phone, address, city):
        self.id = id
        self.name = name
        self.major = major
        self.faculty = faculty
        self.user_role = user_role
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "major": self.major,
            "faculty": self.faculty,
            "user_role": self.user_role,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "city": self.city
        }


def update_user_info(User):
    try:
        cnx = mysql.connector.connect(user='root', password="0931588846hP",
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        password = stauth.Hasher(User.password).generate()
        query = f"UPDATE user_info SET name = '{User.name}', major = '{User.major}', faculty = '{User.faculty}', user_role = '{User.user_role}', username = '{User.username}', password = '{password[-1]}', email = '{User.email}', phone = '{User.phone}', address = '{User.address}', city = '{User.city}' WHERE id = '{User.id}';"
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        cnx.close()
    except ValueError:
        print("User info is not valid")


def insert_user_info(User):
    try:
        cnx = mysql.connector.connect(user='root', password="0931588846hP",
                                      host='127.0.0.1', port=3306,
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        password = stauth.Hasher(User.password).generate()
        print(password, type(password))
        query = f"INSERT INTO user_info (id, name, major, faculty, user_role, username, password, email, phone, address, city) VALUES ('{User.id}', '{User.name}', '{User.major}', '{User.faculty}', '{User.user_role}', '{User.username}', '{password[-1]}', '{User.email}', '{User.phone}', '{User.address}', '{User.city}')"
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        cnx.close()
    except ValueError:
        print("User info is not valid")


def get_all_user():
    all_user = []
    try:
        cnx = mysql.connector.connect(user='root', password=password_db,
                                      host='127.0.0.1', port=3306,
                                      database='test')
        cursor = cnx.cursor(buffered=True)

        query = "SELECT * FROM user_info"
        cursor.execute(query)
        for (id, name, major, faculty, user_role, username, password, email, phone, address, city) in cursor:
            all_user.append(User(id, name, major, faculty, user_role,
                            username, password, email, phone, address, city).to_dict())
        cursor.close()
        cnx.close()
    except ValueError:
        print("All user info is not valid")

    return all_user


def delete_user_by_id(id):
    try:
        cnx = mysql.connector.connect(user='root', password=password_db,
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)

        query = f"DELETE FROM user_info WHERE id = '{id}';"
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        cnx.close()
    except ValueError:
        st.error("Some things went wrong")


def get_user_by_username(username):
    get_all_user()
    for user in get_all_user():
        if user['username'] == username:
            return user


def get_user_by_id(id):
    get_all_user()
    for user in get_all_user():
        if user['id'] == id:
            return user


def get_user_by_major(major):
    get_all_user()
    all_user = []
    i = 0
    for user in get_all_user():
        if user['major'] == major and user['user_role'] != 'Giáo viên':
            all_user.append(user['name'])
    return all_user


def get_user_not_euqal_admin():
    get_all_user()
    all_user = []
    for user in get_all_user():
        if user['user_role'] != 'admin':
            all_user.append(user['name'])
    return all_user


def get_user_by_name(name):
    get_all_user()
    for user in get_all_user():
        if user['name'] == name:
            return user


id = np.random.randint(100000000, 999999999)
# id = '123456789'
# insert_user_info(User(id, "Trung", "Việt Nhật", "Công nghệ thông tin",
#                  "Học sinh", "4", "1", "", "", "", ""))

# insert_user_info(User(id, "Duy Anh", "Computer Science",
#                  "Science", "Giáo viên", "1", "1", "1", "1", "1", "1"))
