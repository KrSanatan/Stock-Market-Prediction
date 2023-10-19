# -*- coding: utf-8 -*-
"""StockPricePrediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1R0QtTTs7dnXVwUbbroQT6N78UthMmD7y
"""



"""# **Stock Market Prediction and Forecasting using Stacked LSTM**"""

#using keras and tensorflow

#Data Collection
import pandas_datareader as pdr

key = '0fd52ed6ff4942ab6ae94a0b0cd72add481f9d43'
df = pdr.get_data_tiingo('AAPL',api_key=key)

df.to_csv('AAPL.csv')

df.head()

import pandas as pd

df.tail()

#taking close column and for that we are performing stock prediction
df1 = df.reset_index()['close']

df1.shape

#plotting this close data frame
import matplotlib.pyplot as plt
plt.plot(df1)

#LSTM being sensitive to the scale of data hence applying MinMax scalar
#transforming values between 0 to 1

import numpy as np

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))
df1 = scaler.fit_transform(np.array(df1).reshape(-1,1))

#df1 will be converted into an array with values 0 to 1
df1

#splitting dataset into train and test set
training_size=int(len(df1)*0.65)
test_size=len(df1)-training_size
train_data,test_data=df1[0:training_size,:],df1[training_size:len(df1),:1]

training_size,test_size

import numpy
#converting an array of values into a dataset matrix
def create_dataset(dataset,time_step=1):
  dataX,dataY =[],[]
  for i in range(len(dataset)-time_step-1):
    a = dataset[i:(i+time_step),0]
    dataX.append(a)
    dataY.append(dataset[i+time_step,0])
  return numpy.array(dataX),numpy.array(dataY)

#reshape into X=t,t+1,t+2... and Y=t+4
time_step=100
x_train,y_train=create_dataset(train_data,time_step)
x_test,y_test=create_dataset(test_data,time_step)

print(x_train)

print(x_train.shape)

#reshaping input to be [samples,time steps, features] as per the LSTM requirement
x_train = x_train.reshape(x_train.shape[0],x_train.shape[1],1)
x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], 1)

#creating the stacked LSTM model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM

model = Sequential()
model.add(LSTM(50,return_sequences=True,input_shape=(100,1)))
model.add(LSTM(50,return_sequences=True))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(loss='mean_squared_error',optimizer='adam')

model.summary()

model.fit(x_train,y_train,validation_data=(x_test,y_test),epochs=100,batch_size=64,verbose=1)

import tensorflow as tf

tf.__version__

#prediction and performance metrics
train_predict = model.predict(x_train)
test_predict = model.predict(x_test)

#transform back to original form -- reverse scaling
train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)

#calculating RMSE performance matrics
import math
from sklearn.metrics import mean_squared_error
math.sqrt(mean_squared_error(y_train,train_predict))

#test data RMSE
math.sqrt(mean_squared_error(y_test,test_predict))

#plotting
#shift train predictions for plotting
look_back=100
trainPredictPlot=numpy.empty_like(df1)
trainPredictPlot[:, :]=np.nan
trainPredictPlot[look_back:len(train_predict)+look_back, :]=train_predict
#shift test predictions for plotting
testPredictPlot=numpy.empty_like(df1)
testPredictPlot[:, :]=numpy.nan
testPredictPlot[len(train_predict)+(look_back*2)+1:len(df1)-1, :]=test_predict
#plotting baseline and predcitions
plt.plot(scaler.inverse_transform(df1))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()

#predicting future 30 days

len(test_data)

x_input=test_data[340:].reshape(1,-1)

x_input.shape

temp_input=list(x_input)
temp_input=temp_input[0].tolist()

#demonstrating prediction for next 30 days
from numpy import array

lst_output=[]
n_steps=100
i=0
while(i<30):
  if(len(temp_input)>100):
    x_input=np.array(temp_input[1:])
    x_input=x_input.reshape(1,-1)
    x_input=x_input.reshape((1,n_steps,1))
    yhat=model.predict(x_input,verbose=0)
    temp_input.extend(yhat[0].tolist())
    temp_input=temp_input[1:]
    lst_output.extend(yhat.tolist())
    i=i+1
  else:
    x_input=x_input.reshape((1,n_steps,1))
    yhat=model.predict(x_input,verbose=0)
    temp_input.extend(yhat[0].tolist())
    lst_output.extend(yhat.tolist())
    i=i+1

day_new=np.arange(1,101)
day_pred=np.arange(101,131)

import matplotlib.pyplot as plt

len(df1)

df3=df1.tolist()
df3.extend(lst_output)

plt.plot(day_new,scaler.inverse_transform(df1[1156:]))
plt.plot(day_pred,scaler.inverse_transform(lst_output))

df3=df1.tolist()
df3.extend(lst_output)
plt.plot(df3[1000:])

