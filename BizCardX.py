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

if st.button("Extract Data and save to DB"):
    np_image = np.array(denoised_image)
    result = reader.readtext(np_image)
    for text in result:
        extracted_lines.append(text[1])
    extracted_text = "\n".join(extracted_lines)
    st.subheader("Extracted Text")
    st.write(extracted_text)
    st.write(extracted_lines)

#
    pattern = r'(\w+)\s+\w+\s+\d{6}\s+(\w+)\s*$'

    match = re.search(pattern, extracted_text, re.IGNORECASE)

    if match:
        first_name = match.group(1)
        second_name = match.group(2)
        full_name = first_name + " " + second_name
        st.write("Company Name:", full_name)
    else:
        st.write("Names not found in the text.")

#

    name_pattern = r'^\w+'
    match = re.search(name_pattern, extracted_text)

    if match:
        first_name = match.group()
        st.write("Card Holder Name:", first_name)
    else:
        st.write("No names found in the text.")

#

    designation_pattern = r'^\w+\s+(\w+)\s+(\w+)'
    designation_name = re.search(designation_pattern, extracted_text)
    
    if designation_name:
        second_word = designation_name.group(1)
        third_word = designation_name.group(2)
        designation = f"{second_word} {third_word}"
        st.write("Designation:", designation)
   
#
 
    phone_pattern = r'\+\d{3}-\d{3}-\d{4}'
    phone_numbers = re.findall(phone_pattern, extracted_text)

    if phone_numbers and len(phone_numbers) == 2:
        p1, p2 = phone_numbers
        st.write("Phone Number 1:", p1)
        st.write("Phone Number 2:", p2)
                                                              
#
    
    website_pattern = r'www[\w\-]+\.com'
    website = re.search(website_pattern, extracted_text)

    if website:
        website_name = website.group()
        st.write("Website:", website_name)
        
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
  
#    
    state_pattern = r',\s*(?:\w+\s+)([^,]+)\s+(\d{6})'
    state_name = re.search(state_pattern, extracted_text)
    
    if state_name:
        state = state_name.group(1).strip()
        postal_code = state_name.group(2)
        st.write("State:", state)
        st.write("Postal Code:", postal_code)
       
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
        Company_name VARCHAR(255) NOT NULL,
        Card_Holder_name VARCHAR(255) NOT NULL,
        designation VARCHAR(15),
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

connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "12345",
    database = "cards"
)
cursor = connection.cursor()
   
insert_statement = """
INSERT INTO company_info (
    Company_name,
    Card_Holder_name,
    designation,
    phone1,
    phone2,
    website,
    email,
    address,
    city,
    state,
    postal_code,
    additional_info
) 
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)"""

data_to_insert = (
    full_name,
    first_name,
    designation,
    p1,
    p2,
    website_name,
    email_id,
    addresses,
    cities,
    state,
    postal_code,
    extracted_text
)

cursor.execute(insert_statement, data_to_insert)

connection.commit()

connection.close()