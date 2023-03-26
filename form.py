import datetime as dt
import streamlit as st
import numpy as np
import db_user
import db_attendence
import db_class
from PIL import Image
from process import *
path = "C:/Users/chauk/OneDrive/Máy tính/New folder/Web-Reconig/"

dayofweeks = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]


def add_new_user(user_info):
    with st.form("add_new_student"):
        id = np.random.randint(100000000, 999999999)
        name = st.text_input("Họ và tên", "")

        if user_info["user_role"] == "Giáo viên":

            major = st.selectbox(
                "Khoa", (user_info["major"], ""))
            faculty = st.selectbox(
                "Ngành", (user_info["faculty"], ""))
            user_role = st.selectbox("Quyền", ("Sinh viên", ""))

            username = "#"
            password = "#"

        elif user_info["user_role"] == "Admin":
            faculty = st.selectbox(
                "Ngành", db_class.get_unique_faculty())
            if faculty:
                major = st.selectbox(
                    "Khoa", db_class.get_major_by_faculty(faculty))

            user_role = st.selectbox(
                "Quyền", ("Giáo viên", "Admin"))
            username = st.text_input("Tên đăng nhập", "")

            password = st.text_input("Mật khẩu", "")

        email = st.text_input("Email", "")
        phone = st.text_input("Số điện thoại", "")
        address = st.text_input("Địa chỉ", "")
        city = st.text_input("Thành phố", "")
        col1, col2, col3, col4, col5 = st.columns(5)

        with col3:
            if st.form_submit_button("Thêm"):
                user = db_user.User(id, name, major, faculty, user_role,
                                    username, password, email, phone, address, city)
                if user.user_role == 'Sinh viên':
                    TakeImages(path, user)
                    st.success("Thêm sinh viên thành công")
                elif user.user_role == 'Giáo viên':
                    db_user.insert_user_info(user)
                    st.success("Thêm giáo viên thành công")
                elif user.user_role == 'Admin':
                    db_user.insert_user_info(user)
                    st.success("Thêm Admin thành công")
                st.balloons()


def change_info_user(user_info):
    with st.form("change_info_student"):
        if user_info["user_role"] == "Giáo viên":
            name_of_students = db_user.get_user_by_major(
                user_info["major"])
            select_name = st.sidebar.selectbox(
                "Tên học sinh", name_of_students)
        elif user_info["user_role"] == "Admin":
            name_of_users = db_user.get_user_not_euqal_admin()
            select_name = st.selectbox("Tên người dùng", name_of_users)

        user_info = db_user.get_user_by_name(select_name)

        id = user_info['id']
        name = st.text_input("Tên", user_info['name'])
        major = st.selectbox(
            "Ngành", (user_info["major"], ""))
        faculty = st.selectbox(
            "Khoa", (user_info["faculty"], ""))
        user_role = st.selectbox("Quyền", (user_info["user_role"], ""))

        username = ""
        password = ""

        # username = st.text_input("Tên đăng nhập", user_info["username"])
        # password = st.text_input("Mật khẩu", user_info["password"])
        email = st.text_input("Email", user_info["email"])
        phone = st.text_input("Số điện thoại", user_info["phone"])
        address = st.text_input("Địa chỉ", user_info["address"])
        city = st.text_input("Thành phố", user_info["city"])
        col1, col2, col3, col4, col5 = st.columns(5)

        with col3:
            if st.form_submit_button("Thay đổi"):
                new_info_student = db_user.User(
                    id, name, major, faculty, user_role, username, password, email, phone, address, city)
                db_user.update_user_info(new_info_student)
                st.balloons()
                st.success("Thay đổi thành công")


def delete_user(user_info):
    if user_info["user_role"] == "Giáo viên":
        name_of_students = db_user.get_user_by_major(
            user_info["major"])
        user = st.sidebar.selectbox("Tên sinh viên", name_of_students)
    elif user_info["user_role"] == "Admin":
        name_of_students = db_user.get_user_not_euqal_admin()
        user = st.selectbox("Tên người dùng", name_of_students)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col3:
        if st.button("Xóa"):
            user_info = db_user.get_user_by_name(user)
            major = st.sidebar.selectbox("Ngành", (user_info["major"], ""))
            faculty = st.sidebar.selectbox(
                "Khoa", (user_info["faculty"], ""))
            db_user.delete_user_by_id(user_info['id'])
            st.balloons()
            st.success("Xóa thành công")


def account(user_info):

    with st.form("account"):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:
            image = Image.open(path+'ImageIcon/account.png')
            st.image(image)

        id = user_info['id']
        name = st.text_input("Họ và tên", user_info['name'])
        major = st.selectbox(
            "Ngành", (user_info["major"], ""))
        faculty = st.selectbox(
            "Khoa", (user_info["faculty"], ""))
        user_role = st.selectbox("Quyền", (user_info["user_role"], ""))
        username = st.text_input("Tên đăng nhập", user_info["username"])
        password = st.text_input("Mật khẩu", user_info["password"])
        email = st.text_input("Email", user_info["email"])
        phone = st.text_input("Số điện thoại", user_info["phone"])
        address = st.text_input("Địa chỉ", user_info["address"])
        city = st.text_input("Thành phố", user_info["city"])
        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:
            if st.form_submit_button("Thay đổi"):
                try:
                    db_user.update_user_info(db_user.User(
                        id, name, major, faculty, user_role, username, password, email, phone, address, city))
                    st.balloons()
                    st.success("Thay đổi thành công")
                except:
                    st.error("Thất bại")


def add_new_class(user_info):
    with st.form("add_new_class"):
        id = np.random.randint(100000000, 999999999)
        class_name = st.text_input("Tên lớp", "")
        major = st.selectbox("Ngành", (user_info["major"], ""))
        faculty = st.selectbox("Khoa", (user_info["faculty"], ""))
        time = st.time_input("Thời gian bắt đầu", dt.time(8, 45))
        time_end = st.time_input("Thời gian kết thúc", dt.time(10, 45))
        dayofweek = st.selectbox(
            "Thứ", ("Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"))
        students = st.multiselect(
            "Danh sách học sinh", db_user.get_user_by_major(user_info["major"]))
        teacher = user_info["id"]
        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:
            if st.form_submit_button("Thêm lớp"):
                list_id_student = ""
                # print(students, list_id_student)
                for student in students:
                    list_id_student += str(db_user.get_user_by_name(student)
                                           ["id"]) + ","
                db_class.insert_new_class(db_class.Class(
                    id, class_name, major, faculty, time, time_end, dayofweek, list_id_student, teacher))
                st.balloons()
                st.success("Thêm lớp thành công")


def change_class_info(user_info):
    classes = db_class.get_class_by_teacher(user_info["id"])
    class_name = st.selectbox("Tên lớp", classes)
    class_info = db_class.get_class_by_class_name(class_name)

    student_id_list = class_info["students"].split(",")
    student_id_list.pop(-1)
    student_name_list = []
    for student_id in student_id_list:
        student_id = int(student_id)
        student_name_list.append(db_user.get_user_by_id(student_id)["name"])

    with st.form("change_class_info"):
        class_name = st.text_input("Tên lớp", class_info["class_name"])
        major = st.selectbox("Ngành", (class_info["major"], ""))
        faculty = st.selectbox("Khoa", (class_info["faculty"], ""))

        time = st.time_input("Thời gian bắt đầu", dt.datetime.strptime(
            class_info["time"], '%H:%M:%S'))
        time_end = st.time_input("Thời gian kết thúc", dt.datetime.strptime(
            class_info["time_end"], '%H:%M:%S'))
        dayofweek = st.text_input("Thứ", class_info["dayofweek"])
        students = st.multiselect(
            "Danh sách học sinh", db_user.get_user_by_major(user_info["major"]), default=student_name_list)
        teacher = user_info["id"]
        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:
            if st.form_submit_button("Thay đổi"):
                list_id_student = ""

                for student in students:
                    list_id_student += str(db_user.get_user_by_name(student)
                                           ["id"]) + ","
                db_class.update_class_info(db_class.Class(
                    class_info["id"], class_name, major, faculty, time, time_end, dayofweek, list_id_student, teacher))
                st.balloons()
                st.success("Thay đổi thành công")


def delete_class(user_info):
    classes = db_class.get_class_by_teacher(user_info["id"])
    class_name = st.selectbox("Tên lớp", classes)
    class_info = db_class.get_class_by_class_name(class_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col3:
        if st.button("Xóa"):
            db_class.delete_class_by_id(int(class_info["id"]))
            st.balloons()
            st.success("Xóa thành công")
