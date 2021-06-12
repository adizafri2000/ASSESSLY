import streamlit as st
import pandas as pd
from assesly import *

#RE-OPEN TERMINAL IN VSCODE BY: CTRL + ` 

st.title('ASSESSLY Analysis')

NAME_COLUMN = 'Student Name'
EXPECTED_FILE_HEADERS = ['Student Name','Class','E1','E2','E3','Final','Quiz','Attendance']
TEST_LIST = ['E1','E2','E3','Final','Quiz','Attendance']
subject_name = ''
PAGE_SECTIONS = [
    'Received Data',
    'Student Performance on Test vs Test Comparison',
    'Analysis per Individual Student',
    'Overall Student Performance for Subject Tests',
    'Performance by Class',
    'Performance by Test'
]

#Counter for streamlit selectbox widget to assign its unique key to avoid DuplicateWidgetID error
selectbox_count = 0

#To add a gap between sections in the webpage
def section_gap():
    st.markdown('#')

# To add a line break between sections in webpage
def section_separator():
    section_gap()
    st.write('---')
    section_gap()
    
# Loads xlsx to data frame
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

# XLSX FILE UPLOAD SECTION : UNDER CONSTRUCTION AND CONSIDERATION !!
st.header('Data file upload')
st.info(
    'ASSESSLY currently only supports files in **.xlsx format** and **must contain these header columns**: '+
    '*Student Name, Class, E1, E2, E3, Final, Quiz, Attendance*. If there are multiple sheets in the .xlsx file, only the '+
    '***first sheet will be analysed***.'
)
uploaded_file = st.file_uploader("Choose your student data file:",type='xlsx')
file_accepted = False
if uploaded_file is not None:
    if file_validator(uploaded_file):
        st.success('Uploaded file is validated by system.')
        file_accepted = True
        uploaded_file = load_data(uploaded_file)
    else:
        st.error('File invalid. Make sure column header names follow the expected format: **Student Name, Class, E1, E2, E3, Final, Quiz, Attendance**')

if file_accepted:

    #SUBJECT NAME INPUT
    subject_name = st.text_input('Enter name of subject')

    if subject_name != '' and len(subject_name.split())!=0:
        section_separator()
        add_sidebar()

        #RAW XLSX FILE
        st.header('Data for subject: '+subject_name)
        st.header(PAGE_SECTIONS[0])
        st.write(uploaded_file)

        section_separator()

        #CLUSTERING SECTION
        st.header(PAGE_SECTIONS[1])
        c1 = st.selectbox('Test 1/Attendance selection:',TEST_LIST,index=0,key=selectbox_unique_key())
        c2 = st.selectbox('Test 2/Attendance selection:',[x for x in TEST_LIST if x!=c1],key=selectbox_unique_key())
        section_gap()
        st.write('Viewing overall student performance for **' + subject_name + ' - ' + c1 + ' vs ' + c2+ '**:')
        st.plotly_chart(getClustering(uploaded_file,c1,c2))

        section_separator()

        #INDIVIDUAL STUDENT ANALYSIS ON SUBJECT SECTION
        st.header(PAGE_SECTIONS[2])
        student_list = uploaded_file[NAME_COLUMN]
        student_selection = st.selectbox('Select a student:',student_list,key=selectbox_unique_key())
        section_gap()
        st.write('Viewing **' + student_selection + '**\'s performance on {} tests:'.format(subject_name))
        st.plotly_chart(showStudentPerformance(uploaded_file,student_selection))

        section_separator()

        #OVERALL STUDENT PERFORMANCE FOR SUBJECT ON A TEST TYPE SECTION
        st.header(PAGE_SECTIONS[3])
        test_selection = st.selectbox('Select a test type or attendance record:',TEST_LIST,key=selectbox_unique_key())
        section_gap()
        st.write('Viewing overall student performance for **'+ subject_name + ' ' + test_selection + '**:')
        st.plotly_chart(Overallperformance(uploaded_file,test_selection))

        student_below_min, student_below_lower_quartile = getLowPerformanceStudent(uploaded_file,test_selection)
        shown_columns = [x for x in EXPECTED_FILE_HEADERS if x in EXPECTED_FILE_HEADERS[:2] or x==test_selection]
        st.write('Students between Quartile 1 and Lower Fence:')
        st.write('*{} student{} in total.*'.format(len(student_below_lower_quartile),' ' if len(student_below_lower_quartile)==1 else 's'))
        st.write(student_below_lower_quartile[shown_columns])
        section_gap()
        st.write('**Students Below Lower Fence:**')
        st.write('*{} student{} in total.*'.format(len(student_below_min),' ' if len(student_below_min)==1 else 's'))
        if len(student_below_min)>0:
            st.write(student_below_min[shown_columns])

        section_separator()

        #Performance by class section
        st.header(PAGE_SECTIONS[4])
        class_test_selection = st.selectbox('Select a test type or attendance record:',TEST_LIST,key=selectbox_unique_key())
        st.write('Viewing performance by class on **'+ subject_name + ' ' + class_test_selection + '**:')
        st.plotly_chart(performanceByClass(uploaded_file,class_test_selection))
        section_gap()
        st.write('Average of each classes on **{} {}**:'.format(subject_name,class_test_selection))
        st.write(getAverageByClass(uploaded_file,class_test_selection))

        section_separator()

        # Performance by Test section
        st.header(PAGE_SECTIONS[5])
        st.write('Viewing performance by test on {}\'s tests:'.format(subject_name))
        st.plotly_chart(perFormancebyTest(uploaded_file))
        test_performance_analysis = getPerformancebyTest(uploaded_file)
        st.write(test_performance_analysis)

        #BACK TO TOP
        section_gap()
        st.write('[Back to top](#assessly-analysis)')

