import mysql.connector
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import streamlit as st

def get_user_info(id):
    db_user_json = None
    try:
        cnx = mysql.connector.connect(user='root', password='12345678hP.',
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)

        querry = f"SELECT * FROM user_info where id = {id}"
        cursor.execute(querry)
        for (id, name, department, position, username, password, email, phone, address, city) in cursor:
            db_user_json = {"id": id, "name": name, "department": department, "position": position, "username": username,
                            "password": password, "email": email, "phone": phone, "address": address, "city": city}
        cursor.close()
        cnx.close()
    except ValueError:
        print("Invalid ID")

    return db_user_json


def update_user_info(id, name, department, position, username, password, email, phone, address, city):
    try:
        cnx = mysql.connector.connect(user='root', password='12345678hP.',
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        password = stauth.Hasher(password).generate()
        querry = f"UPDATE user_info SET name = '{name}', username = '{username}', password = '{password[-1]}', email = '{email}', phone = '{phone}', address = '{address}', city = '{city}' where id = '{id}'"
        cursor.execute(querry)
        cnx.commit()
        cursor.close()
        cnx.close()
    except ValueError:
        print("User info is not valid")


def insert_user_info(id, name, department, position, username, password, email, phone, address, city):
    try:
        cnx = mysql.connector.connect(user='root', password='12345678hP.',
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        password = stauth.Hasher(password).generate()
        querry = f"INSERT INTO user_info (id, name, department, position, username, password, email, phone, address, city) VALUES ('{id}', '{name}', '{department}', '{position}', '{username}', '{password[-1]}', '{email}', '{phone}', '{address}', '{city}')"
        cursor.execute(querry)
        cnx.commit()
        cursor.close()
        cnx.close()
    except ValueError:
        print("User info is not valid")


def get_all_user():
    db_all_user_info = []
    try:
        cnx = mysql.connector.connect(user='root', password='12345678hP.',
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        querry = "SELECT * FROM user_info"
        cursor.execute(querry)
        for (id, name, department, position, username, password, email, phone, address, city) in cursor:
            db_user_json = {"id": id, "name": name, "department": department, "position": position, "username": username,
                            "password": password, "email": email, "phone": phone, "address": address, "city": city}
            db_all_user_info.append(db_user_json)
        cursor.close()
        cnx.close()
    except ValueError:
        print("All user info is not valid")

    return db_all_user_info


def get_user_by_username(username):
    db_user_json = None
    try:
        cnx = mysql.connector.connect(user='root', password='12345678hP.',
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        querry = "SELECT * FROM user_info where username = '{}'".format(
            username)
        cursor.execute(querry)
        for (id, name, department, position, username, password, email, phone, address, city) in cursor:
            db_user_json = {"id": id, "name": name, "department": department, "position": position, "username": username,
                            "password": password, "email": email, "phone": phone, "address": address, "city": city}
        cursor.close()
        cnx.close()
    except ValueError:
        print("All user info is not valid")

    return db_user_json

def get_user_by_name(name):
    db_user_json = None
    try:
        cnx = mysql.connector.connect(user='root', password='12345678hP.',
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        querry = "SELECT * FROM user_info where name = '{}'".format(
            name)
        cursor.execute(querry)
        for (id, name, department, position, username, password, email, phone, address, city) in cursor:
            db_user_json = {"id": id, "name": name, "department": department, "position": position, "username": username,
                            "password": password, "email": email, "phone": phone, "address": address, "city": city}
        cursor.close()
        cnx.close()
    except ValueError:
        print("User info is not valid")

    return db_user_json

def get_all_unique_name():
    names = []
    try:
        cnx = mysql.connector.connect(user='root', password='12345678hP.',
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)

        querry = "SELECT DISTINCT name FROM user_info;"
        cursor.execute(querry)

        for (name) in cursor:
            names.append(name[0])
        cursor.close()
        cnx.close()
    except ValueError:
        pass

    return tuple(names)


def get_all_unique_name_by_department(department):
    names = []
    try:
        cnx = mysql.connector.connect(user='root', password='12345678hP.',
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)

        querry = f"SELECT DISTINCT name FROM user_info where position = 'Staff' and department = '{department}';"
        cursor.execute(querry)

        for (name) in cursor:
            names.append(name[0])
        cursor.close()
        cnx.close()
    except ValueError:
        pass

    return tuple(names)

def delete_user_by_id(id):
    try:
        cnx = mysql.connector.connect(user='root', password='12345678hP.',
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)

        querry = f"DELETE FROM user_info WHERE id = '{id}';"
        cursor.execute(querry)
        cnx.commit()
        cursor.close()
        cnx.close()
    except ValueError:
        st.error("Some things went wrong")

# insert_user_info(290307480, "Nurul", "IT", "Staff", "a", "1", "nurul@gmail.com", "017000", "Dhaka", "Dhaka")
# db_all_user_info = get_all_user()
# print(db_all_user_info)

# insert_user_info(2, "admin", "admin", "admic", "admin", "1", "1", "1", "1", "1")
# print(get_all_unique_name_by_department('Marketing'))

# print(get_user_by_name("Le Khac Chau"))