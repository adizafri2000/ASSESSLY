import time
import streamlit as st
import pandas as pd
import numpy as np
import openpyxl as pyxl
from assesly_old import *

#RE-OPEN TERMINAL IN VSCODE BY: CTRL + ` 

st.title('ASSESSLY Analysis')

#DATA_FILE = 'Book1.xlsx'
NAME_COLUMN = 'Student Name'
subject_dictionary = {
    'Mathematics' : student_result_maths,
    'Science': student_result_science,
    'Sejarah': student_result_sejarah 
}
EXPECTED_FILE_HEADERS = ['Student Name','Class','E1','E2','E3','Final','Quiz','Attendance']
TEST_LIST = ['E1','E2','E3','Final','Quiz']
PAGE_SECTIONS = [
    'Extracted raw data',
    'Student Performance on Test vs Test Comparison',
    'Analysis per Individual Student',
    'Overall Student Performance for Subject Tests',
    'Performance by Class'
]
subject_name = ''

#Counter for streamlit selectbox widget to assign its unique key to avoid DuplicateWidgetID error
selectbox_count = 0

#To add a gap between sections in the webpage
def section_gap():
    st.markdown('#')

# To add a line break between sections in webpage
def section_separator():
    st.write('---')
    
#@st.cache
def load_data(file_selection):
    with st.spinner('Loading data ...'):
        data = pd.read_excel(file_selection)
        return data

# Validates the .xlsx file by checking the header format - 
# Student Name, Class, E1, E2, E3, Final, Quiz, Attendance
def file_validator(data_file):
    data_file = pd.read_excel(data_file)
    return True if data_file.columns.tolist()==EXPECTED_FILE_HEADERS else False

# Generates unique key ID for streamlit selectbox widget via counter variable
def selectbox_unique_key():
    global selectbox_count
    current_key = selectbox_count
    selectbox_count+=1
    return current_key

def add_sidebar():
    sb = st.sidebar
    sb.header('Page Navigation')
    for i in range (len(PAGE_SECTIONS)):
        anchor_link = '-'.join(PAGE_SECTIONS[i].lower().split())
        sb.write('***['+PAGE_SECTIONS[i]+'](#'+anchor_link+')***')
    return sb

add_sidebar()

# XLSX FILE UPLOAD SECTION : UNDER CONSTRUCTION AND CONSIDERATION !!
st.subheader('Data file upload')
st.info(
    'ASSESSLY currently only supports files in **.xlsx format** and **must contain these header columns**: '+
    '*Student Name, Class, E1, E2, E3, Final, Quiz, Attendance*. If there are multiple sheets in the .xlsx file, only the '+
    '***first sheet will be analysed***.'
)
uploaded_file = st.file_uploader("Choose your student data file:",type='xlsx')
file_accepted = False
if uploaded_file is not None:
    if file_validator(uploaded_file):
        st.success('File is valid! Sheesh!')
        file_accepted = True
        uploaded_file = load_data(uploaded_file)
    else:
        st.error('File invalid. Make sure column header names are follow expected format')

if file_accepted:

    section_separator()

    #SUBJECT NAME INPUT
    subject_name = st.text_input('Enter name of subject')
    st.write(subject_name)

    if subject_name != '' and len(subject_name.split())!=0:
        temp = subject_name

        section_gap()

        #RAW XLSX FILE
        st.header('Data for subject: '+subject_name)
        st.subheader(PAGE_SECTIONS[0])
        st.write(uploaded_file)

        section_separator()

        #CLUSTERING SECTION
        st.subheader(PAGE_SECTIONS[1])
        c1 = st.selectbox('Test 1 selection:',TEST_LIST,index=0,key=selectbox_unique_key())
        c2 = st.selectbox('Test 2 selection:',[x for x in TEST_LIST if x!=c1],key=selectbox_unique_key())
        section_gap()
        st.write('Viewing overall student performance for ***' + subject_name + ': ' + c1 + ' vs ' + c2+ '***')
        st.plotly_chart(getClustering(uploaded_file,c1,c2))

        section_separator()

        #INDIVIDUAL STUDENT ANALYSIS ON SUBJECT SECTION
        st.subheader(PAGE_SECTIONS[2])
        #student_list = pd.read_excel(uploaded_file,subject_name)[NAME_COLUMN]
        student_list = uploaded_file[NAME_COLUMN]
        student_selection = st.selectbox('Select a student:',student_list,key=selectbox_unique_key())
        section_gap()
        st.subheader(student_selection + '\'s performance')
        st.plotly_chart(showStudentPerformance(uploaded_file,student_selection))

        section_separator()

        #OVERALL STUDENT PERFORMANCE FOR SUBJECT ON A TEST TYPE SECTION
        st.subheader(PAGE_SECTIONS[3])
        test_selection = st.selectbox('Select a test type:',TEST_LIST,key=selectbox_unique_key())
        section_gap()
        st.write('Viewing overall student performance for ***'+ subject_name + ' ' + test_selection + '***')
        st.plotly_chart(Overallperformance(uploaded_file,test_selection))

        section_separator()

        #Performance by class section
        st.subheader(PAGE_SECTIONS[4])
        class_test_selection = st.selectbox('Select a test type:',TEST_LIST,key=selectbox_unique_key())
        st.write('Viewing performance by class on ***'+ subject_name + ' ' + class_test_selection + '***')
        st.plotly_chart(performanceByClass(subject_name,class_test_selection))

        section_gap()

#BACK TO TOP
st.write('[Back to top](#assessly-analysis)')