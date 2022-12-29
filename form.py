import streamlit as st
import numpy as np
import db_user as db_user
import db_department as db_department
import db_don_xin as db_don_xin
from PIL import Image
from process import *
path = "/home/katherinee/Desktop/Job/Web_Reconig/"


def add_new_staff(manage_info):
    with st.form("add_new_staff"):
        id = np.random.randint(100000000, 999999999)
        name = st.text_input("Name", "")
        department = st.selectbox(
            "Department", (manage_info["department"], ""))
        position = st.selectbox("Position", ("Staff", ""))
        username = "staff"
        password = "staff"
        email = st.text_input("Email", "")
        phone = st.text_input("Phone number", "")
        address = st.text_input("Address", "")
        city = st.text_input("City", "")
        col1, col2, col3, col4, col5 = st.columns(5)

        with col3:
            if st.form_submit_button("Summit"):
                # db_user.insert_user_info(
                #     id, name, department, position, username, password, email, phone, address, city)
                TakeImages(
                    path, id, name, department, position, username, password, email, phone, address, city)
                # st.balloons()
                # st.success("Add new staff successfully")


def add_new_staff_for_admin():
    with st.form("add_new_staff"):
        id = np.random.randint(100000000, 999999999)
        name = st.text_input("Name", "")
        department = st.selectbox(
            "Department", db_department.get_all_unique_department())
        position = st.selectbox("Position", ("Staff", ""))
        username = st.text_input("Username", "")
        password = st.text_input("Password", "")
        email = st.text_input("Email", "")
        phone = st.text_input("Phone number", "")
        address = st.text_input("Address", "")
        city = st.text_input("City", "")
        col1, col2, col3, col4, col5 = st.columns(5)

        with col3:
            if st.form_submit_button("Summit"):
                # db_user.insert_user_info(
                #     id, name, department, position, username, password, email, phone, address, city)
                TakeImages(
                    path, id, name, department, position, username, password, email, phone, address, city)
                st.balloons()
                st.success("Add new staff successfully")


def add_new_employeer():
    with st.form("add_new_employeer"):
        id = np.random.randint(100000000, 999999999)
        name = st.text_input("Name", "")
        department = st.selectbox(
            "Department", db_department.get_all_unique_department())
        position = st.selectbox("Position", ("Manager", "Admin"))
        username = st.text_input("Username", "")
        password = st.text_input("Password", "")
        email = st.text_input("Email", "")
        phone = st.text_input("Phone number", "")
        address = st.text_input("Address", "")
        city = st.text_input("City", "")
        col1, col2, col3, col4, col5 = st.columns(5)

        with col3:
            if st.form_submit_button("Summit"):
                # db_user.insert_user_info(
                #     id, name, department, position, username, password, email, phone, address, city)
                TakeImages(
                    path, id, name, department, position, username, password, email, phone, address, city)
                st.balloons()
                st.success("Add new employeer successfully")


def change_info_staff(manage_info):
    user_names = db_user.get_all_unique_name_by_department(
        manage_info["department"])
    select_user_name = st.selectbox("Name of Staff", user_names)
    if select_user_name:
        user_info = db_user.get_user_by_name(select_user_name)
        with st.form("change_info_staff"):
            id = user_info['id']
            name = st.text_input("Name", user_info['name'])
            department = st.selectbox(
                "Department", (user_info["department"], ""))
            position = st.selectbox("Position", (user_info["position"], ""))
            username = st.text_input("Username", user_info["username"])
            password = st.text_input("Password", user_info["password"])
            email = st.text_input("Email", user_info["email"])
            phone = st.text_input("Phone number", user_info["phone"])
            address = st.text_input("Address", user_info["address"])
            city = st.text_input("City", user_info["city"])
            col1, col2, col3, col4, col5 = st.columns(5)

            with col3:
                if st.form_submit_button("Change"):
                    db_user.update_user_info(
                        id, name, department, position, username, password, email, phone, address, city)
                    st.balloons()
                    st.success("Update is successfull")


def change_info():
    user_names = db_user.get_all_unique_name()
    select_user_name = st.sidebar.selectbox("Name of employeers", user_names)
    if select_user_name:
        user_info = db_user.get_user_by_name(select_user_name)
        with st.form("change_info"):
            id = user_info['id']
            name = st.text_input("Name", user_info['name'])

            department = st.selectbox(
                "Department", (user_info["department"], ""))
            # st.session_state["department"] = user_info["department"]
            print(department == user_info["department"])
            position = st.selectbox("Position", (user_info["position"], ""))
            # st.session_state["positon"] = user_info["positon"]

            username = st.text_input("Username", user_info["username"])
            password = st.text_input("Password", user_info["password"])
            email = st.text_input("Email", user_info["email"])
            phone = st.text_input("Phone number", user_info["phone"])
            address = st.text_input("Address", user_info["address"])
            city = st.text_input("City", user_info["city"])
            col1, col2, col3, col4, col5 = st.columns(5)

            with col3:
                if st.form_submit_button("Change"):
                    db_user.update_user_info(
                        id, name, department, position, username, password, email, phone, address, city)
                    st.balloons()
                    st.success("Update is successfull")


def detlete_staff(manage_info):
    user_names = db_user.get_all_unique_name_by_department(
        manage_info["department"])
    select_user_name = st.sidebar.selectbox("Name of Staff", user_names)
    department = st.selectbox("Department", (manage_info["department"], ""))
    col1, col2, col3, col4, col5 = st.columns(5)

    with col3:
        if st.button("Detele"):
            user_info = db_user.get_user_by_name(select_user_name)
            db_user.delete_user_by_id(user_info['id'])
            st.balloons()
            st.success("Delete success")


def detlete_user():
    user_names = db_user.get_all_unique_name()
    select_user_name = st.sidebar.selectbox("Name of Staff", user_names)
    if select_user_name:
        user_info = db_user.get_user_by_name(select_user_name)
        department = st.selectbox("Department", (user_info["department"], ""))
        position = st.selectbox("Position", (user_info["position"], ""))
        phone = st.write("Phone number:", user_info["phone"])
        address = st.write("Address:", user_info["address"])
        city = st.write("City:", user_info["city"])
    col1, col2, col3, col4, col5 = st.columns(5)

    with col3:
        if st.button("Detele"):
            user_info = db_user.get_user_by_name(select_user_name)
            db_user.delete_user_by_id(user_info['id'])
            st.balloons()
            st.success("Delete success")


def account(user_info):

    with st.form("account"):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:
            image = Image.open('ImageIcon/account.png')
            st.image(image)

        id = user_info['id']
        name = st.text_input("Name", user_info['name'])
        department = st.selectbox(
            "Department", (user_info["department"], ""))

        position = st.selectbox("Position", (user_info["position"], ""))
        username = st.text_input("Username", user_info["username"])
        password = st.text_input("Password", user_info["password"])
        email = st.text_input("Email", user_info["email"])
        phone = st.text_input("Phone number", user_info["phone"])
        address = st.text_input("Address", user_info["address"])
        city = st.text_input("City", user_info["city"])
        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:
            if st.form_submit_button("Change"):
                db_user.update_user_info(
                    id, name, department, position, username, password, email, phone, address, city)
                st.balloons()
                st.success("Update is successfull")

def don_nghi(user_info):
    id = np.random.randint(100000, 999999)
    with st.form("don_nghi"):
        name = st.selectbox("Loai don", ("Nghi om", "Nghi viec", "Xin nghi phep", "Xin den muon", "Xin ve som"))
        ten_nhan_vien = st.text_input("Ten nhan vien", user_info['name'])
        bo_phan = st.text_input("Bo phan", user_info['department'])
        vi_tri = st.text_input("Vi tri", user_info['position'])
        ngay_bat_dau = st.date_input("Ngay nghi")
        ngay_ket_thuc = st.date_input("Ngay ket thuc")
        ly_do = st.text_input("Ly do")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:
            if st.form_submit_button("Gui don"):
                db_don_xin.insert_don_nghi(id, name, ten_nhan_vien, bo_phan, vi_tri, ngay_bat_dau,ngay_ket_thuc, ly_do)