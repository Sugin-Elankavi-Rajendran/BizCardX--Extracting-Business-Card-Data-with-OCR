import streamlit as st
import easyocr
from PIL import Image
import io
import tempfile

##########################

st.title ("BizCardX Data Extraction")
image = st.file_uploader("Choose a business card image", type=["jpg", "png", "jpeg"])

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
