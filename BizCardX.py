import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from system_path import home_image
import easyocr
import mysql.connector
import pandas as pd
import os
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

#Starting easyOCR, connecting MySQL and creating Table
        
reader = easyocr.Reader(['en'])

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="cards"
)

mycursor = mydb.cursor(buffered=True)

mycursor.execute('''CREATE TABLE IF NOT EXISTS card_data
                   (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    company_name TEXT,
                    card_holder TEXT,
                    designation TEXT,
                    mobile_number VARCHAR(50),
                    email TEXT,
                    website TEXT,
                    area TEXT,
                    city TEXT,
                    state TEXT,
                    pin_code VARCHAR(10),
                    image LONGBLOB
                    )''')

#######################################################

#Upload and Extract Option

if selected == "Upload & Extract":
    if st.button(":blue[Already stored data]"):
        mycursor.execute("select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data")
        updated_df = pd.DataFrame(mycursor.fetchall(),
                                  columns=["Company_Name", "Card_Holder", "Designation", "Mobile_Number",
                                           "Email", "Website", "Area", "City", "State", "Pin_Code"])
        st.write(updated_df)
    st.subheader(":blue[Upload a Business Card]")

    uploaded_card = st.file_uploader("Choose a business card image", label_visibility="collapsed", type=["png", "jpeg", "jpg"])

    if uploaded_card is not None:

        def save_card(uploaded_card):
            uploaded_cards_dir = os.path.join(os.getcwd(), "uploaded_cards")
            with open(os.path.join(uploaded_cards_dir, uploaded_card.name), "wb") as f:
                f.write(uploaded_card.getbuffer())

        save_card(uploaded_card)



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

