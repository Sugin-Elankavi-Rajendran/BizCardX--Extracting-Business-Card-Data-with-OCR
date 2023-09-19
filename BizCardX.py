import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import mysql.connector

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

extracted_lines = []

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Extract Text"):
        np_image = np.array(image)
        result = reader.readtext(np_image)
        for text in result:
            extracted_lines.append(text[1])
        extracted_text = "\n".join(extracted_lines)
        st.subheader("Extracted Text")
        st.write(extracted_text)
        st.write(extracted_lines)

#######################

connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "12345",
    database = "cards"
)
cursor = connection.cursor()

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
