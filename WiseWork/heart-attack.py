import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
import joblib

df = pd.read_csv('heart.csv')

x = df.drop(['output'],axis = 1)
y = df['output']
xtrain,xtest,ytrain,ytest = train_test_split(x,y,test_size = 0.2, random_state = 42)
sc = StandardScaler()
xtrain  =  sc.fit_transform(xtrain)
xtest = sc.fit_transform(xtest)
kn = KNeighborsClassifier(n_neighbors=5)
kn.fit(xtrain,ytrain)

y_pred = kn.predict(xtest)
print(kn.score(xtest,ytest) * 100)
print(kn.score(xtest,ytest) * 100)

filename = 'finalized_model.sav'
joblib.dump(kn, filename)