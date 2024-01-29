import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from system_path import home_image
import pandas as pd
import easyocr
import cv2
import mysql.connector
import numpy as np
import re

#######################################################

#option menu

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>BizCardX Data Extraction</h1>", unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu("Main Menu", ["Home","Upload & Extract","Modify"], 
        icons=["house","cloud-upload","pencil-square"], menu_icon="cast", default_index=1)
    selected

#######################################################

#Home Option

if selected == "Home":
    col1 , col2 = st.columns(2)
    with col1:
        st.image(Image.open(home_image))
    with col2:
        st.write("")
        st.markdown(
        """
        To extract card details, click the "Upload & Extract" option.
        """
        )   
        st.write("")
        st.markdown(
        """
        To modify the details in the database, click the "Modify" option.
        """
        )

#######################################################
   
# image = st.file_uploader("Choose a business card image", type=["jpg", "png", "jpeg"])

# if st.button("Extract"):
#     if image:
#         img = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
#         reader = easyocr.Reader(["en"], gpu=False)
#         results = reader.readtext(img)
#         col1, col2 = st.columns(2)
#         col1.image(image, caption="Original Business Card", use_column_width=True)
#         col2.image(img, caption="Processed Business Card", use_column_width=True)
        
#         answer = []
#         for result in results:
#             answer.append(result[1])
#         st.write(answer)

# #######################################################

# selected = option_menu(None, ["Home","Upload & Extract","Modify"],
#                        icons=["house","cloud-upload","pencil-square"],
#                        default_index=0,
#                        orientation="horizontal",
#                        styles={"nav-link": {"font-size": "35px", "text-align": "centre", "margin": "-2px", "--hover-color": "#6495ED"},
#                                "icon": {"font-size": "35px"},
#                                "container" : {"max-width": "6000px"},
#                                "nav-link-selected": {"background-color": "#6495ED"}})

# ##########################################################

#         email_pattern = r"\b[A-Za-z0-9.+_%-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
#         emails = []
#         for result in results:
#             m = result[1]
#             found_emails = re.findall(email_pattern, m)
#             emails.extend(found_emails)

#         st.write("E-Mail:", emails[0])

# ##########################################################

#         website_pattern = r"(\S+\.com)\b"
#         website = []
#         for result in results:
#             w = result[1]
#             websites = re.findall(website_pattern, w, flags=re.IGNORECASE)
#             website.extend(websites)
#         final_website = []
#         for web in website:
#             if "@" not in web:
#                 final_website.append(web)
        
#         st.write("Website URLs:", final_website[0])

# ##########################################################
        
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="12345",
#     database="cards"
# )

# mycursor = mydb.cursor()

# mycursor.execute("""
#     CREATE TABLE IF NOT EXISTS card_info (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         company_name VARCHAR(255),
#         card_holder_name VARCHAR(255),
#         designation VARCHAR(255),
#         mobile_number INT,
#         phone_number INT,
#         email_address VARCHAR(255),
#         website_URL VARCHAR(255),
#         area VARCHAR(255),
#         city VARCHAR(255),
#         state VARCHAR(255),
#         pincode INT
#     )
# """)

# sql = "INSERT INTO card_info (company_name, card_holder_name, designation, mobile_number, phone_number, email_address, website_URL, area, city, state, pincode) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
