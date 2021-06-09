import streamlit as st
import pandas as pd
import numpy as np
import openpyxl as pyxl
from assesly import *

#RE-OPEN TERMINAL IN VSCODE BY: CTRL + ` 

st.title('ASSESSLY Analysis')

FINAL_COLUMN = 'Final'
DATA_FILE = ('Book1.xlsx')
NAME_COLUMN = 'Student Name'
subject_dictionary = {
    'Mathematics' : student_result_maths,
    'Science': student_result_science,
    'Sejarah': student_result_sejarah 
}
TEST_LIST = ('E1','E2','E3','Final','Quiz')

@st.cache
def load_data(sheet_selection):
    data = pd.read_excel(DATA_FILE, sheet_name=sheet_selection)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    #data[FINAL_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

#DATA LOAD FOR SUBJECT SECTION
sheet_selection = st.selectbox('Subject',('Mathematics','Science','Sejarah'))
data = load_data(sheet_selection)

#RAW XLSX FILE
st.subheader('Data for subject: '+sheet_selection)
st.subheader('Raw data')
st.write(data)

#CLUSTERING SECTION
c1 = st.selectbox('Test 1 selection',TEST_LIST)
c2 = st.selectbox('Test 2 selection',TEST_LIST)
st.subheader('Overall Student Performance on ' + sheet_selection + ': ' + c1 + ' vs ' + c2)
st.plotly_chart(getClustering(subject_dictionary[sheet_selection],c1,c2))

#INDIVIDUAL STUDENT ANALYSIS ON SUBJECT SECTION
st.subheader('Analysis per Individual Student')
student_list = pd.read_excel(DATA_FILE,sheet_selection)[NAME_COLUMN]
student_selection = st.selectbox('Student name',student_list)
st.subheader(student_selection + '\'s performance')
st.plotly_chart(showStudentPerformance(student_selection))

#OVERALL STUDENT PERFORMANCE FOR SUBJECT ON A TEST TYPE SECTION
test_selection = st.selectbox('Test selection',TEST_LIST)
st.subheader('Overall Student Performance for '+ sheet_selection + ' ' + test_selection)
st.plotly_chart(Overallperformance(subject_dictionary[sheet_selection],test_selection))