import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import mysql.connector
import cv2
import tempfile
import re


###############

reader = easyocr.Reader(['en'])

###############

st.set_page_config(layout="wide")
st.title("Business Card Detail Extraction:")
uploaded_file = st.file_uploader(
    "Upload the Business Card",
    type= ['png', 'jpg'],
    accept_multiple_files=False,
    label_visibility="visible"
)

###############

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name
    image = cv2.imread(temp_file_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
    denoised_image = cv2.fastNlMeansDenoising(binary_image, None, h=10, templateWindowSize=7, searchWindowSize=21)
 
###############

if uploaded_file and denoised_image is not None:
    cols = st.columns(2)
    with cols[0]:
        st.image(uploaded_file, use_column_width=True, caption="Uploaded Image")
    with cols[1]:
        st.image(denoised_image, use_column_width=True, caption="Processed Image")

###############

extracted_lines = []

if st.button("Extract Text"):
    np_image = np.array(denoised_image)
    result = reader.readtext(np_image)
    for text in result:
        extracted_lines.append(text[1])
    extracted_text = "\n".join(extracted_lines)
    st.subheader("Extracted Text")
    st.write(extracted_text)
    st.write(extracted_lines)

#
    
    website_pattern = r'www[\w\-]+\.com'
    website = re.search(website_pattern, extracted_text)

    if website:
        website_name = website.group()
        st.write("Website:", website_name)
   
#
 
    phone_pattern = r'\+\d{3}-\d{3}-\d{4}'
    phone_numbers = re.findall(phone_pattern, extracted_text)
    
    if phone_numbers:
        for phone_number in phone_numbers:
            st.write("Phone Number:", phone_number)

#
    
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    email = re.search(email_pattern, extracted_text)
    
    if email:
        email_id = email.group()
        st.write("Email Address:", email_id)

#
    
    address_pattern = r'\d+\s+ABC St'
    address_name = re.search(address_pattern, extracted_text)
    
    if address_name:
        addresses = address_name.group()
        st.write("Address:", addresses)

#
    
    city_pattern = r',\s*([A-Za-z\s]+)'
    city_name = re.search(city_pattern, extracted_text)
    
    if city_name:
        cities = city_name.group(1)
        st.write("City:", cities)
          
#######################

connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "12345",
    database = "cards"
)
cursor = connection.cursor()

table_exists = False
cursor.execute("SHOW TABLES LIKE 'company_info'")
if cursor.fetchone():
    table_exists = True
    
if not table_exists:
    create_table_for_company_info = """
    CREATE TABLE company_info (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        phone1 VARCHAR(15),
        phone2 VARCHAR(15),
        website VARCHAR(255),
        email VARCHAR(255),
        address VARCHAR(255),
        city VARCHAR(255),
        state VARCHAR(255),
        postal_code VARCHAR(10),
        additional_info TEXT
    )"""
    
    cursor.execute(create_table_for_company_info)

connection.commit()
connection.close()

#################################

