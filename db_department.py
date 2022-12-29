import mysql.connector
import numpy as np


def get_all_unique_department():
    departments = []
    try:
        cnx = mysql.connector.connect(user='root', password='12345678hP.',
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)

        querry = "SELECT DISTINCT department FROM department;"
        cursor.execute(querry)

        for (department) in cursor:
            departments.append(department[0])
        cursor.close()
        cnx.close()
    except ValueError:
        pass

    return tuple(departments)


def insert_new_department(department, position):
    id = np.random.randint(100000000, 999999999)

    try:
        cnx = mysql.connector.connect(user='root', password='12345678hP.',
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)

        querry = f"INSERT INTO department (id, department, position) VALUES ('{id}', '{department}', '{position}')"
        cursor.execute(querry)
        cnx.commit()
        cursor.close()
        cnx.close()
    except ValueError:
        pass

        
# insert_new_department("Customer care", "Manger")
