import streamlit as st
import easyocr
import cv2
import mysql.connector
import numpy as np
import re

#######################################################

st.set_page_config(layout="wide")
st.title("BizCardX Data Extraction")
image = st.file_uploader("Choose a business card image", type=["jpg", "png", "jpeg"])

if st.button("Extract"):
    if image:
        img = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
        reader = easyocr.Reader(["en"], gpu=False)
        results = reader.readtext(img)
        col1, col2 = st.columns(2)
        col1.image(image, caption="Original Business Card", use_column_width=True)
        col2.image(img, caption="Processed Business Card", use_column_width=True)
        
        answer = []
        for result in results:
            answer.append(result[1])
        st.write(answer)

##########################################################

        email_pattern = r"\b[A-Za-z0-9.+_%-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        emails = []
        for result in results:
            m = result[1]
            found_emails = re.findall(email_pattern, m)
            emails.extend(found_emails)

        st.write("E-Mail:", emails[0])

##########################################################
        
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="cards"
)

mycursor = mydb.cursor()

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS card_info (
        id INT AUTO_INCREMENT PRIMARY KEY,
        company_name VARCHAR(255),
        card_holder_name VARCHAR(255),
        designation VARCHAR(255),
        mobile_number INT,
        phone_number INT,
        email_address VARCHAR(255),
        website_URL VARCHAR(255),
        area VARCHAR(255),
        city VARCHAR(255),
        state VARCHAR(255),
        pincode INT
    )
""")

sql = "INSERT INTO card_info (company_name, card_holder_name, designation, mobile_number, phone_number, email_address, website_URL, area, city, state, pincode) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
