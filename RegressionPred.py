#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 14:50:40 2019

@author: vishal
"""

import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime
from sklearn.linear_model import LinearRegression, LogisticRegression
import matplotlib.pyplot as plt
from IPython import get_ipython
import pickle 
#get_ipython().run_line_magic('matplotlib', 'inline')

df = pd.read_csv('StudentData.csv')

'''
fig, ax = plt.subplots()
#df.hist('Math', ax=ax)
#fig.savefig('MathScores.png')
#df.hist('Biology', ax=ax)
#fig.savefig('BioScores.png')
#df.hist('Chemistry', ax=ax)
#fig.savefig('ChemScores.png')
df.hist('Computer Science', ax=ax)
fig.savefig('CSScores.png')
'''
'''
R1 = 'Chemistry'
R2 = 'Biology'
fig, ax = plt.subplots()
ax.grid(True)
plt.xlabel(R1)
plt.ylabel(R2)
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.plot(df[R1], df[R2])
fig.savefig(R1+"_vs_"+R2+".png")
'''

Ch = df.iloc[:, 4].values.reshape(-1, 1)
B = df.iloc[:, 5].values.reshape(-1, 1)  
linear_regressorCB = LinearRegression()  
linear_regressorCB.fit(Ch, B)  

linear_regressorBC = LinearRegression()  
linear_regressorBC.fit(B, Ch)  

M = df.iloc[:, 3].values.reshape(-1, 1)  
CS = df.iloc[:, 6].values.reshape(-1, 1) 
linear_regressorCM = LinearRegression()  
linear_regressorCM.fit(M, CS)  

linear_regressorMC = LinearRegression()  
linear_regressorMC.fit(CS, M)  

S = df.iloc[:, 7].values.reshape(-1, 1)
logistic_regressorMS = LogisticRegression()  
logistic_regressorMS.fit(M, S)

logistic_regressorSC = LogisticRegression()
logistic_regressorSC.fit(CS, S)  

pkl_filename = "Models/CB.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(linear_regressorCB, file, protocol=2)

pkl_filename = "Models/BC.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(linear_regressorBC, file, protocol=2)

pkl_filename = "Models/CM.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(linear_regressorCM, file, protocol=2)

pkl_filename = "Models/MC.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(linear_regressorMC, file, protocol=2)

pkl_filename = "Models/MS.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(logistic_regressorMS, file, protocol=2)

pkl_filename = "Models/SC.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(logistic_regressorSC, file, protocol=2)

