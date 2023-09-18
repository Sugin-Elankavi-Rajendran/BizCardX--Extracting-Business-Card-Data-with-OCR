import streamlit as st
import easyocr
import sqlite3
from PIL import Image
import io

# Create a SQLite database to store extracted information
conn = sqlite3.connect('business_cards.db')
cursor = conn.cursor()

# Create a table to store business card data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS business_cards (
        id INTEGER PRIMARY KEY,
        company_name TEXT,
        card_holder_name TEXT,
        designation TEXT,
        mobile_number TEXT,
        email_address TEXT,
        website_url TEXT,
        area TEXT,
        city TEXT,
        state TEXT,
        pin_code TEXT,
        image BLOB
    )
''')
conn.commit()

# Function to extract information from an image using easyOCR
def extract_info(image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    
    info = {
        'company_name': '',
        'card_holder_name': '',
        'designation': '',
        'mobile_number': '',
        'email_address': '',
        'website_url': '',
        'area': '',
        'city': '',
        'state': '',
        'pin_code': ''
    }
    
    for detection in result:
        text = detection[1]
        if 'Company' in text:
            info['company_name'] = text
        elif 'Name' in text:
            info['card_holder_name'] = text
        elif 'Designation' in text:
            info['designation'] = text
        elif 'Mobile' in text:
            info['mobile_number'] = text
        elif 'Email' in text:
            info['email_address'] = text
        elif 'Website' in text:
            info['website_url'] = text
        elif 'Area' in text:
            info['area'] = text
        elif 'City' in text:
            info['city'] = text
        elif 'State' in text:
            info['state'] = text
        elif 'Pin' in text:
            info['pin_code'] = text
    
    return info

# Streamlit UI
st.title("Business Card Information Extractor")

# Upload image
uploaded_image = st.file_uploader("Upload a business card image", type=["jpg", "jpeg", "png"])
if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Business Card", use_column_width=True)
    
    if st.button("Extract Information"):
        extracted_info = extract_info(image)
        st.subheader("Extracted Information:")
        for key, value in extracted_info.items():
            st.write(f"{key}: {value}")
        
        if st.button("Save to Database"):
            # Convert the image to bytes
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")
            image_bytes = image_bytes.getvalue()
            
            # Insert data into the database
            cursor.execute('''
                INSERT INTO business_cards
                (company_name, card_holder_name, designation, mobile_number, email_address, website_url,
                area, city, state, pin_code, image)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (extracted_info['company_name'], extracted_info['card_holder_name'], extracted_info['designation'],
                  extracted_info['mobile_number'], extracted_info['email_address'], extracted_info['website_url'],
                  extracted_info['area'], extracted_info['city'], extracted_info['state'], extracted_info['pin_code'],
                  image_bytes))
            
            conn.commit()
            st.success("Information saved to the database.")

# Read data from the database
if st.button("Read Data from Database"):
    cursor.execute('SELECT * FROM business_cards')
    data = cursor.fetchall()
    
    st.subheader("Data in the Database:")
    for row in data:
        card_id, company_name, card_holder_name, designation, _, _, _, area, city, state, pin_code, _ = row
        st.write(f"Card ID: {card_id}")
        st.write(f"Company Name: {company_name}")
        st.write(f"Card Holder Name: {card_holder_name}")
        st.write(f"Designation: {designation}")
        st.write(f"Area: {area}")
        st.write(f"City: {city}")
        st.write(f"State: {state}")
        st.write(f"Pin Code: {pin_code}")
        st.image(Image.open(io.BytesIO(row[-1])), caption="Business Card Image", use_column_width=True)

# Update and Delete data can be added similarly.

# Close the database connection
conn.close()
