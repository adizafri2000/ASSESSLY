import streamlit as st
import pandas as pd
import numpy as np
import openpyxl as pyxl

#RE-OPEN TERMINAL IN VSCODE BY: CTRL + ` 

st.title('ASSESSLY Analysis')

FINAL_COLUMN = 'Final'
DATA_FILE = ('Book1.xlsx')
NAME_COLUMN = 'Student Name'

@st.cache
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
st.subheader('Raw data')
st.write(data)

st.subheader('Analysis per Individual Student')

student_list = pd.read_excel(DATA_FILE,sheet_selection)[NAME_COLUMN]
student_selection = st.selectbox('Student name',student_list)
st.subheader(student_selection + '\'s performance')
from assesly import *
st.plotly_chart(showStudentPerformance(student_selection))

#TO DO: BRING THE FIGURE IN THE JUPYTER NOTEBOOK FILE TO STREAMLIT