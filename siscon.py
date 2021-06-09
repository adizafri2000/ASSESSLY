import streamlit as st
import pandas as pd
import numpy as np
import openpyxl as pyxl

#RE-OPEN TERMINAL BY: CTRL + `

st.title('ASSESSLY Analysis')

FINAL_COLUMN = 'Final'
DATA_FILE = ('Book1.xlsx')

def load_data(sheet_selection):
    data = pd.read_excel(DATA_FILE, sheet_name=sheet_selection)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    #data[FINAL_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

#enables user to select sheet on the xlsx file
sheet_selection = st.selectbox('Subject',('Mathematics','Science','Sejarah'))

data_load_state = st.text('Loading data...')
data = load_data(sheet_selection)
data_load_state.text("Done!")

st.subheader('Data for subject: '+sheet_selection)
st.write(data)