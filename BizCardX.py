import streamlit as st

###############

st.set_page_config(layout="wide")
st.header("Business Card Detail Extraction:")
uploaded_file = st.file_uploader(
    "Upload the Business Card",
    type= ['png', 'jpg'],
    accept_multiple_files=False, 
    key=None, 
    help=None, 
    on_change=None, 
    args=None, 
    kwargs=None,
    disabled=False, 
    label_visibility="visible"
)