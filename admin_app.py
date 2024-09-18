import streamlit as st
import pandas as pd

from export_csv import export


st.title("Скачать файл solutions.csv")

st.download_button(
    label="Скачать CSV",
    data=export(save=False).to_csv(index=False),
    file_name='solutions.csv',
    mime='text/csv'
)
