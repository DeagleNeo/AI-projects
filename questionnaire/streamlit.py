import streamlit as st

name = st.text_input("Enter your name:")
if st.button("Submit"):
    st.write(f"Hello, {name}!")
