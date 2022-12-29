import mysql.connector
import datetime
from datetime import datetime

def insert_don_xin(Id, name, ten_nhan_vien, bo_phan, vi_tri, ngay_bat_dau, ngay_ket_thuc, ghi_chu):
    try:
        cnx = mysql.connector.connect(user='root', password='12345678hP.',
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        query = "INSERT INTO don_xin (Id, name, ten_nhan_vien, bo_phan, vi_tri, ngay_bat_dau, ngay_ket_thuc, ghi_chu) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (Id, name, ten_nhan_vien, bo_phan, vi_tri, ngay_bat_dau, ngay_ket_thuc, ghi_chu))
        cnx.commit()
        cursor.close()
        cnx.close()
        
    except ValueError:
        print("Invalid input")

def get_all_don_xin():
    try:
        cnx = mysql.connector.connect(user='root', password='12345678hP.',
                                      host='127.0.0.1',
                                      database='test')
        cursor = cnx.cursor(buffered=True)
        query = "SELECT * FROM don_xin"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return result
    except ValueError:
        print("Invalid input")


