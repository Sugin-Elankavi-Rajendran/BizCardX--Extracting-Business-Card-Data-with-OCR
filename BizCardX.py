import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from system_path import home_image
import easyocr
import mysql.connector
import pandas as pd
import os
import cv2
import matplotlib.pyplot as plt
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
            uploaded_cards_dir = "uploaded_cards"
            file_path = os.path.join(uploaded_cards_dir, uploaded_card.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_card.getbuffer())

        save_card(uploaded_card)

        def image_preview(image, res):
            for bbox, text, prob in res:
                tl, tr, br, bl = map(lambda p: (int(p[0]), int(p[1])), bbox)
                cv2.rectangle(image, tl, br, (0, 255, 0), 2)
                cv2.putText(image, text, (tl[0], tl[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            plt.figure(figsize=(15, 15))
            plt.axis('off')
            plt.imshow(image)
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("#     ")
            st.markdown("#     ")
            st.markdown("### You have uploaded the card")
            st.image(uploaded_card)
        
        with col2:
            st.markdown("#     ")
            st.markdown("#     ")
            with st.spinner("Please wait processing image..."):
                st.set_option('deprecation.showPyplotGlobalUse', False)
                saved_img = os.path.join(os.getcwd(), "uploaded_cards", uploaded_card.name)
                image = cv2.imread(saved_img)
                res = reader.readtext(saved_img)
                st.markdown("### Image Processed and Data Extracted")
                st.pyplot(image_preview(image, res))

        saved_img = os.path.join(os.getcwd(), "uploaded_cards", uploaded_card.name)
        result = reader.readtext(saved_img, detail=0, paragraph=False)

        def img_to_binary(file):
            with open(file, 'rb') as file:
                binaryData = file.read()
            return binaryData
        
        data = {"company_name": [],
                "card_holder": [],
                "designation": [],
                "mobile_number": [],
                "email": [],
                "website": [],
                "area": [],
                "city": [],
                "state": [],
                "pin_code": [],
                "image": img_to_binary(saved_img)
                }
        
        def get_data(res):
            for ind, i in enumerate(res):

                # To get WEBSITE
                if "www " in i.lower() or "www." in i.lower():
                    data["website"].append(i)
                elif "WWW" in i:
                    data["website"] = res[4] + "." + res[5]

                # To get EMAIL-ID
                elif "@" in i:
                    data["email"].append(i)

                # To get MOBILE NUMBER
                elif "-" in i:
                    data["mobile_number"].append(i)
                    if len(data["mobile_number"]) == 2:
                        data["mobile_number"] = " & ".join(data["mobile_number"])

                # To get COMPANY NAME
                elif ind == len(res) - 1:
                    data["company_name"].append(i)

                # To get CARD HOLDER NAME
                elif ind == 0:
                    data["card_holder"].append(i)

                # To get DESIGNATION
                elif ind == 1:
                    data["designation"].append(i)

                # To get AREA
                if re.findall('^[0-9].+, [a-zA-Z]+', i):
                    data["area"].append(i.split(',')[0])
                elif re.findall('[0-9] [a-zA-Z]+', i):
                    data["area"].append(i)

                # To get CITY NAME
                match1 = re.findall('.+St , ([a-zA-Z]+).+', i)
                match2 = re.findall('.+St,, ([a-zA-Z]+).+', i)
                match3 = re.findall('^[E].*', i)
                if match1:
                    data["city"].append(match1[0])
                elif match2:
                    data["city"].append(match2[0])
                elif match3:
                    data["city"].append(match3[0])

                # To get STATE
                state_match = re.findall('[a-zA-Z]{9} +[0-9]', i)
                if state_match:
                    data["state"].append(i[:9])
                elif re.findall('^[0-9].+, ([a-zA-Z]+);', i):
                    data["state"].append(i.split()[-1])
                if len(data["state"]) == 2:
                    data["state"].pop(0)

                # To get PINCODE
                if len(i) >= 6 and i.isdigit():
                    data["pin_code"].append(i)
                elif re.findall('[a-zA-Z]{9} +[0-9]', i):
                    data["pin_code"].append(i[10:])

        get_data(result)

        def create_df(data):
            df = pd.DataFrame(data)
            return df
        
        df = create_df(data)
        st.success("### Data Extracted!")
        st.write(df)

        if st.button("Upload to Database"):
            for i, row in df.iterrows():
                sql = """INSERT INTO card_data(company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code,image)
                         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                mycursor.execute(sql, tuple(row))
                mydb.commit()
                st.success("#### Uploaded to database successfully!")
        
        if st.button(":blue[View updated data]"):
            mycursor.execute("select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data")
            updated_df = pd.DataFrame(mycursor.fetchall(),
                                          columns=["Company_Name", "Card_Holder", "Designation", "Mobile_Number",
                                                   "Email",
                                                   "Website", "Area", "City", "State", "Pin_Code"])
            st.write(updated_df)

#######################################################

# Modify Option
            


