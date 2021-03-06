# -*- coding: utf-8 -*-
"""ASSESLY.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18iELkuvKD_dSyKnPlWDBYc831-GgPXwS
"""

import pandas as pd
import plotly.express as px

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

"""# Import data """

# import data from xlsx to dataframe

#student_result_maths = pd.read_excel (r'/content/StudentResult_Mathematics.xlsx')
#student_result_science = pd.read_excel (r'/content/StudentResult_Science.xlsx')
#student_result_sejarah = pd.read_excel (r'/content/StudentResult_Sejarah.xlsx')


student_result_maths = pd.read_excel (r'content\StudentResult_Mathematics.xlsx')
student_result_science = pd.read_excel (r'content\StudentResult_Science.xlsx')
student_result_sejarah = pd.read_excel (r'content\StudentResult_Sejarah.xlsx')

"""# Clustering

## Clustering function
"""

'''
df = subject excel file (dataframe)
c1 = test selection 1
c2 = test selection 2
'''
def getClustering(df,c1,c2):
  # get column for clustering
  data = df[[c1,c2]]

  # apply standard scalar on data
  ss = StandardScaler()
  X = ss.fit_transform(data)

  #fit data into model
  model = KMeans(n_clusters=4, verbose=0)
  result = model.fit_predict(X)

  #get the label
  df['Performance Group'] = result.tolist()
  df['Performance Group'] = df['Performance Group'].apply(str)
  df['Performance Group'].replace({"0": "A", "1": "B", "2": "C", "3": "D"}, inplace=True)

  #display
  figClustering = px.scatter(df, x=c1, y=c2,color="Performance Group", hover_data=['Student Name',c1])
  figClustering.update_traces(marker={'size': 10})    

  return figClustering

"""# student performance individual"""

def showStudentPerformance(subject, name):
  studentData = subject.loc[subject['Student Name']==name]

  x = ['E1', 'E2', 'E3','Final']
  y = studentData.iloc[:,2:6].values.ravel()
  hoverLabel = []
  for index,i in enumerate(x):
    hoverLabel.append(i+" Marks = "+str(y[index]))

  figStudentPerformance = px.bar(x=x, y=y, labels=dict(x="Test Type", y="Marks"))
  figStudentPerformance.update_traces(marker_color="#9467BD", hovertemplate=hoverLabel)
  return figStudentPerformance

"""# Overall"""

def Overallperformance(subject, test):
  figOverall = px.box(subject, y=test, points="all",  boxmode="overlay", hover_data=["Student Name"], title=test+" TEST RESULT")
  return figOverall

"""# Performance by class"""

def performanceByClass(subject, test):
  figOverallbyClass = px.box(student_result_maths,x="Class", y=test, points="all",  boxmode="overlay", hover_data=["Student Name"],color="Class", title="Quiz"+" TEST RESULT")
  return figOverallbyClass
