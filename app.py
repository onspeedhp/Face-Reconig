from streamlit_option_menu import option_menu
import time
import csv
import os
# from attendence import attendence_student, attendence_teacher
import streamlit.components.v1 as components
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
from streamlit_option_menu import option_menu
import numpy as np
from process import TakeImages, Attendence
import db_user as db_user
import db_attendance as db_attendance
from form import *

st.set_page_config(page_title="Attendance",
                   page_icon=":bar_chart:", layout="wide")


path = "/home/katherinee/Desktop/Job/Web_Reconig/"

users = db_user.get_all_user()

usernames = [user["username"] for user in users]
names = [user["name"] for user in users]
hashed_passwords = [user["password"] for user in users]

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
                                    "attendance_dashboard", "abcdef", cookie_expiry_days=0)

placeholder = st.empty()
placeholder_menu = st.empty()
placeholder_page = st.empty()

with placeholder_menu:
    selected = option_menu(
        menu_title=None,  # required
        options=["Home", "Attendance", "Log in"],  # required
        icons=["house", "file-person-fill", "box-arrow-in-right"],  # optional
        menu_icon="cast",  # optional
        default_index=0,  # optional
        orientation="horizontal", key="home_page"
    )

if selected == "Home":

    image = Image.open(f'{path}ImageIcon/background.jpg')

    st.image(image)

elif selected == "Attendance":
    image = Image.open(f'{path}ImageIcon/attendance.png')

    st.image(image)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col3:
        if st.button("Take Attendance"):
            Attendence()
            st.balloons()



elif selected == "Log in":
    
    name, authentication_status, username = authenticator.login(
        "Login", "main")
    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Please enter your username and password")

    if authentication_status:
        user_info = db_user.get_user_by_username(username)
        if user_info["position"] == "Staff":
            st.error("You do not have permission to log in to the system")
            placeholder_menu.empty()
            placeholder.empty()

            @st.cache
            def load_data():
                df = db_attendance.get_all_user_attendance()
                df = pd.DataFrame(df)
                df = df[df["department"] == department]
                return df

            name = user_info["name"]
            st.sidebar.title(f"Welcome {name}")
            
            selected = option_menu(
                menu_title=None,  # required
                options=["Form", "Account"],  # required
                icons=["file-person-fill", "file-person-fill"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
                orientation="horizontal", key="options_for_manage"
            )
            if selected == "Form":
                don_nghi(user_info)

            elif selected == "Account":
                account(user_info)
                st.snow()

            authenticator.logout("Logout", "sidebar")

        elif user_info["position"] == "Manager":
            department = user_info["department"]
            placeholder_menu.empty()
            placeholder.empty()

            @st.cache
            def load_data():
                df = db_attendance.get_all_user_attendance()
                df = pd.DataFrame(df)
                df = df[df["department"] == department]
                return df

            def convert_df(df):
                return df.to_csv().encode("utf-8")

            name = user_info["name"]
            st.sidebar.title(f"Welcome {name}")
            
            selected = option_menu(
                menu_title=None,  # required
                options=["Form","Manage", "Statistic", "Account"],  # required
                icons=["house","house", "file-person-fill", "file-person-fill"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
                orientation="horizontal", key="options_for_manage"
            )
            if selected == "Form":
                don_nghi(user_info)
            if selected == "Manage":
                choose = st.selectbox("What do you wants", ["Add new Staff", "Change info Staff", "Delete Staff"])
                if choose == "Add new Staff":
                    add_new_staff(user_info)
                elif choose == "Change info Staff":
                    change_info_staff(user_info)
                elif choose == "Delete Staff":
                    detlete_staff(user_info)
            elif selected == "Statistic":
                df = load_data()    

                st.sidebar.header("Please Filter Here:")

                date = st.sidebar.multiselect(
                    "Select Date:",
                    options=df["date"].unique(),
                    default=df["date"].unique(),
                )
                

                # ---- MAINPAGE ----
                st.title(":bar_chart: Statistic Dashboard")
                st.markdown("##")

                df = df[df["date"].isin(date)]

                st.table(pd.DataFrame(df))

                csv = convert_df(df)
                department = user_info["department"]
                st.download_button(
                    label=f"Download attendance for {department} data as CSV",
                    data=csv,
                    file_name=f"Attendance_{department}.csv",
                    mime="text/csv",
                )

            elif selected == "Account":
                account(user_info)

            authenticator.logout("Logout", "sidebar")

        elif user_info["position"] == "Admin":
            placeholder_menu.empty()
            placeholder.empty()

            @st.cache
            def load_data():
                df = db_attendance.get_all_user_attendance()
                return pd.DataFrame(df)

            def convert_df(df):
                return df.to_csv().encode("utf-8")
            
            
            name = user_info["name"]
            st.sidebar.title(f"Welcome {name}")

            selected = option_menu(
                menu_title=None,  # required
                options=["Manage", "Statistic", "Account"],  # required
                icons=["house", "file-person-fill", "house"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
                orientation="horizontal", key="options_for_admin"
            )
            if selected == "Manage":
                choose = st.sidebar.selectbox("What do you wants", ["Add new Staff","Add new Admin or Manager", "Change info employeer", "Delete employeer"])
                if choose == "Add new Admin or Manager":
                    add_new_employeer()
                elif choose == "Add new Staff":
                    add_new_staff_for_admin()
                elif choose == "Change info employeer":
                    change_info()
                elif choose == "Delete employeer":
                    detlete_user()
            elif selected == "Account":
                account(user_info)
            elif selected == "Statistic":
                

                df = load_data()    

                st.sidebar.header("Please Filter Here:")
                department = st.sidebar.multiselect(
                    "Select the Department:",
                    options=df["department"].unique(),
                    default=df["department"].unique()
                )

                position = st.sidebar.multiselect(
                    "Select Position:",
                    options=df["position"].unique(),
                    default=df["position"].unique(),
                )

                date = st.sidebar.multiselect(
                    "Select Date:",
                    options=df["date"].unique(),
                    default=df["date"].unique(),
                )
                

                # ---- MAINPAGE ----
                st.title(":bar_chart: Statistic Dashboard")
                st.markdown("##")

                df = df[df["department"].isin(department) & df["position"].isin(position) & df["date"].isin(date)]

                st.table(pd.DataFrame(df))

                csv = convert_df(df)
                
                st.download_button(
                    label="Download attendance data as CSV",
                    data=csv,
                    file_name="Attendance.csv",
                    mime="text/csv",
                )

            authenticator.logout("Logout", "sidebar")


