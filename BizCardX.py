import streamlit as st

###############

st.set_page_config(layout="wide")
st.header("Business Card Details Extraction:")
label = "Upload the Business Card"
st.file_uploader(
    label,
    type= ['png', 'jpg'],
    accept_multiple_files=False, 
    key=None, 
    help=None, 
    on_change=None, 
    args=None, 
    kwargs=None, 
    *, 
    disabled=False, 
    label_visibility="visible"
)