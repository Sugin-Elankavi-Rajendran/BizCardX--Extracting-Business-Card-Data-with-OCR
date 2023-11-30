import streamlit as st
import easyocr
from PIL import Image
import io
import tempfile
import mysql.connector

##########################

st.set_page_config(layout="wide")
st.title ("BizCardX Data Extraction")
image = st.file_uploader("Choose a business card image", type=["jpg", "png", "jpeg"])

if st.button("Extract"):
    if image:
        st.image(image, caption="Uploaded Business Card", use_column_width=True)
        reader = easyocr.Reader(["en"])
        image_bytes = io.BytesIO(image.read())
        image_pil = Image.open(image_bytes)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        image_pil.save(temp_file.name)
        results = reader.readtext(temp_file.name)
        temp_file.close()

        for result in results:
            st.write(result[1])

    else:
        st.write("PLEASE UPLOAD TO EXTRACT DATA")

################

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
            email_address VARCHAR(255),
            website_URL VARCHAR(255),
            area VARCHAR(255),
            city VARCHAR(255),
            state VARCHAR(255),
            pincode INT
        )
    """)

sql = "INSERT INTO card_info (company name, card holder name, designation,mobile number, email addresss, website URL, area, city, state, pincode) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

