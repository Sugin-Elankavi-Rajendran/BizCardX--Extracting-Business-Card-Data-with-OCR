import streamlit as st
import easyocr
from PIL import Image
import numpy as np

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