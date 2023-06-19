import tempfile
import streamlit as st

from libs.pdf import read_pdf

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name
    words = read_pdf(temp_file_path)
    for w in words:
        st.write(w.strip("\n"))
