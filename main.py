import streamlit as st
import pandas as pd
import numpy as np
import openpyxl as pyxl
from assesly import *

#RE-OPEN TERMINAL IN VSCODE BY: CTRL + ` 

st.title('ASSESSLY Analysis')

FINAL_COLUMN = 'Final'
DATA_FILE = 'Book1.xlsx'
NAME_COLUMN = 'Student Name'
subject_dictionary = {
    'Mathematics' : student_result_maths,
    'Science': student_result_science,
    'Sejarah': student_result_sejarah 
}
TEST_LIST = ['E1','E2','E3','Final','Quiz']
PAGE_SECTIONS = [
    'Extracted raw data',
    'Student Performance on Test vs Test Comparison',
    'Analysis per Individual Student',
    'Overall Student Performance for Subject Tests'
]

#To add a gap between sections in the webpage
def section_gap():
    st.markdown('#')

# To add a line break between sections in webpage
def section_separator():
    st.write('---')
    
@st.cache
def load_data(sheet_selection):
    data = pd.read_excel(DATA_FILE, sheet_name=sheet_selection)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    #data[FINAL_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Validates the .xlsx file by checking the header format - 
# Student Name, Class, E1, E2, E3, Final, Quiz, Attendance
def file_validator(data_file):
    EXPECTED_FILE_HEADERS = ['Student Name','Class','E1','E2','E3','Final','Quiz','Attendance']
    data_file = pd.read_excel(data_file)
    return True if data_file.columns.tolist()==EXPECTED_FILE_HEADERS else False

def add_sidebar():
    sb = st.sidebar
    for i in range (len(PAGE_SECTIONS)):
        anchor_link = '-'.join(PAGE_SECTIONS[i].lower().split())
        sb.write('***['+PAGE_SECTIONS[i]+'](#'+anchor_link+')***')
    return sb

add_sidebar()

# XLSX FILE UPLOAD SECTION : UNDER CONSTRUCTION AND CONSIDERATION !!
st.subheader('Data file upload')
st.info(
    'ASSESSLY currently only supports files in **.xlsx format** and **must contain these header columns**: '+
    '*Student Name, Class, E1, E2, E3, Final, Quiz, Attendance*'
)
uploaded_file = st.file_uploader("Choose your student data file:",type='xlsx')
if uploaded_file is not None:
    if file_validator(uploaded_file):
        st.write('File is valid! Sheesh!')
    else:
        st.write('File invalid. Make sure column header names are follow expected format')

section_separator()

#DATA LOAD FOR SUBJECT SECTION
sheet_selection = st.selectbox('Select a subject for an analysis view:',('Mathematics','Science','Sejarah'))
data = load_data(sheet_selection)

section_gap()

#RAW XLSX FILE
st.header('Data for subject: '+sheet_selection)
st.subheader('Extracted raw data')
st.write(data)

section_separator()

#CLUSTERING SECTION
st.subheader('Student Performance on Test vs Test Comparison')
c1 = st.selectbox('Test 1 selection:',TEST_LIST,index=0)
c2 = st.selectbox('Test 2 selection:',[x for x in TEST_LIST if x!=c1])
section_gap()
st.write('Viewing overall student performance for ***' + sheet_selection + ': ' + c1 + ' vs ' + c2+ '***')
st.plotly_chart(getClustering(subject_dictionary[sheet_selection],c1,c2))

section_separator()

#INDIVIDUAL STUDENT ANALYSIS ON SUBJECT SECTION
st.subheader('Analysis per Individual Student')
student_list = pd.read_excel(DATA_FILE,sheet_selection)[NAME_COLUMN]
student_selection = st.selectbox('Select a student:',student_list)
section_gap()
st.subheader(student_selection + '\'s performance')
st.plotly_chart(showStudentPerformance(student_selection))

section_separator()

#OVERALL STUDENT PERFORMANCE FOR SUBJECT ON A TEST TYPE SECTION
st.subheader('Overall Student Performance for Subject Tests')
test_selection = st.selectbox('Select a test type:',TEST_LIST)
section_gap()
st.write('Viewing overall student performance for ***'+ sheet_selection + ' ' + test_selection + '***')
st.plotly_chart(Overallperformance(subject_dictionary[sheet_selection],test_selection))

section_gap()

#BACK TO TOP
st.write('[Back to top](#assessly-analysis)')