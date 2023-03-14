from streamlit_option_menu import option_menu
import csv
import pandas as pd  # pip install pandas openpyxl
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
from streamlit_option_menu import option_menu
import numpy as np
from process import Attendence
from form import *
import db_user
import db_attendance
import db_class
from PIL import Image
from skimage.transform import resize

st.set_page_config(page_title="Attendance",
                   page_icon=":bar_chart:", layout="wide")

# path = "C:/Users/kha/Desktop/Web_Reconig Student/"

path = "C:/Users/chauk/OneDrive/Máy tính/New folder/Web-Reconig/"

users = db_user.get_all_user()

usernames = [user['username'] for user in users]
names = [user['name'] for user in users]
hashed_password = [user['password'] for user in users]

authenticator = stauth.Authenticate(names, usernames, hashed_password,
                                    "attendance_dashboard", "abcdef", cookie_expiry_days=0)

placeholder = st.empty()
placeholder_menu = st.empty()
placeholder_page = st.empty()

with placeholder_menu:
    selected = option_menu(
        menu_title=None,  # required
        options=["Trang chủ", "Đăng nhập"],  # required
        icons=["house", "file-person-fill", "box-arrow-in-right"],  # optional
        menu_icon="cast",  # optional
        default_index=0,  # optional
        orientation="horizontal", key="home_page"
    )

if selected == "Trang chủ":

    image = Image.open(f'{path}ImageIcon/background.jpg')
    image = image.resize((1200, 500))
    st.image(image)

elif selected == "Đăng nhập":

    name, authentication_status, Username = authenticator.login(
        "Đăng nhập", "main")
    if authentication_status == False:
        st.error("Tên đăng nhập/mật khẩu không đúng")

    if authentication_status == None:
        st.warning("Hãy điền tên đăng nhập và mật khẩu")

    if authentication_status:

        user_info = db_user.get_user_by_username(Username)

        if user_info["user_role"] == "Giáo viên":
            faculty = user_info["faculty"]
            placeholder_menu.empty()
            placeholder.empty()

            major = user_info['major']
            @st.cache_data 
            def load_major_from_faculty():
                print(user_info['major'])
                df = db_class.get_class_by_major(user_info["major"])
                df = pd.DataFrame(df)
                return df

            all_class_df = load_major_from_faculty()

            name = user_info["name"]
            st.sidebar.title(f"Chào {name}")

            selected = option_menu(
                menu_title=None,  # required
                options=["Quản lý", "Điểm danh", "Thống kê", "Tài khoản"],  # required
                icons=["house", "file-person-fill", "file-person-fill"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
                orientation="horizontal", key="options_for_manage"
            )

            if selected == "Quản lý":
                choose = st.selectbox("Hãy chọn một thao tác quản lý", [
                                      "Thêm sinh viên", "Thay đổi thông tin", "Xóa sinh viên", "Thêm lớp", "Thay đổi thông tin lớp", "Xóa lớp"])
                if choose == "Thêm sinh viên":
                    add_new_user(user_info)
                elif choose == "Thay đổi thông tin":
                    change_info_user(user_info)
                elif choose == "Xóa sinh viên":
                    delete_user(user_info)
                elif choose == "Thêm lớp":
                    add_new_class(user_info)
                elif choose == "Thay đổi thông tin lớp":
                    change_class_info(user_info)
                elif choose == "Xóa lớp":
                    delete_class(user_info)

            elif selected == "Điểm danh":
                choose_class = st.sidebar.selectbox(
                    'Chọn lớp', all_class_df["class_name"].unique())

                if choose_class:
                    choose_dayofweek = st.sidebar.selectbox(
                        'Chọn thời gian', all_class_df[all_class_df["class_name"] == choose_class]["dayofweek"])

                    if choose_dayofweek:
                        choose_time = st.sidebar.selectbox(
                            'Bắt đầu', all_class_df[(all_class_df["class_name"] == choose_class) & (all_class_df["dayofweek"] == choose_dayofweek)]["time"])
                        choose_time_end = st.sidebar.selectbox(
                            'Kết thúc', all_class_df[(all_class_df["class_name"] == choose_class) & (all_class_df["dayofweek"] == choose_dayofweek)]["time_end"])
                col1, col2, col3, col4, col5 = st.columns(5)
                with col3:
                    class_info = db_class.get_class_by_class_name(choose_class)
                    if st.button("Điểm danh"):
                        Attendence(class_info)

            elif selected == "Thống kê":
                choose_class = st.sidebar.selectbox(
                    'Chọn lớp', all_class_df["class_name"].unique())

                if choose_class:
                    choose_dayofweek = st.sidebar.selectbox(
                        'Chọn thời gian', all_class_df[all_class_df["class_name"] == choose_class]["dayofweek"])

                    if choose_dayofweek:
                        choose_time = st.sidebar.selectbox(
                            'Bắt đầu', all_class_df[(all_class_df["class_name"] == choose_class) & (all_class_df["dayofweek"] == choose_dayofweek)]["time"])
                        choose_time_end = st.sidebar.selectbox(
                            'Kết thúc', all_class_df[(all_class_df["class_name"] == choose_class) & (all_class_df["dayofweek"] == choose_dayofweek)]["time_end"])
                        
                    

                    class_info = db_class.get_class_by_class_name(choose_class)
                    
                    st.sidebar.header("Bộ lọc:")
                    time = datetime.now().strftime("%d_%m_%Y")
                    path_csv = f"{path}Attendance/{class_info['id']}_{time}.csv"
                    df = pd.read_csv(path)

                    name = st.sidebar.multiselect(
                        "Họ và tên:",
                        options=df["Họ và tên"].unique(),
                        default=df["Họ và tên"].unique(),
                    )

                    status = st.sidebar.multiselect(
                        "Trạng thái:",
                        options=df["Trạng thái"].unique(),
                        default=df["Trạng thái"].unique(),
                    )

                    # ---- MAINPAGE ----
                    st.title(":bar_chart: Bảng thống kê")
                    st.markdown("##")

                    df = df[df["Họ và tên"].isin(
                        name) & df["Trạng thái"].isin(status)]

                    st.table(pd.DataFrame(df))
                    # except:
                    #     st.write("Không có dữ liệu điểm danh")

            elif selected == "Tài khoản":
                account(user_info)

            authenticator.logout("Đăng xuất", "sidebar")

        elif user_info["user_role"] == "Admin":
            placeholder_menu.empty()
            placeholder.empty()

            @st.cache_data

            def convert_df(df):
                return df.to_csv().encode("utf-8")
            
            def load_major_from_faculty():
                print(user_info['major'])
                df = db_class.get_class_by_major(user_info["major"])
                df = pd.DataFrame(df)
                return df

            all_class_df = load_major_from_faculty()


            name = user_info["name"]
            st.sidebar.title(f"Chào {name}")

            selected = option_menu(
                menu_title=None,  # required
                options=["Quản lý", "Tài khoản"],  # required
                icons=["house", "file-person-fill", "house"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
                orientation="horizontal", key="options_for_admin"
            )
            if selected == "Quản lý":
                choose = st.sidebar.selectbox("Quản lý", ["Thêm thành viên mới", "Thay đổi thông tin", "Xóa"])
                if choose == "Thêm thành viên mới":
                    add_new_user(user_info)
                elif choose == "Thay đổi thông tin":
                    change_info_user(user_info)
                elif choose == "Xóa thành viên":
                    delete_user(user_info)
            elif selected == "Tài khoản":
                account(user_info)

            authenticator.logout("Đăng xuất", "sidebar")
