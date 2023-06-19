import pandas as pd
import numpy as np
import datetime as dt
from sklearn.preprocessing import StandardScaler
import keras
import cufflinks as cf
cf.go_offline()

# stock = pd.read_csv("../data/meb.csv")
#
# model = keras.models.load_model("../forecast/models/model0.h5")

def to_Timestamp(x):
    return dt.datetime.strptime(x.strftime('%Y%m%d'), '%Y%m%d')



#Now the Xtrain contains all of the given dataset ,
# where as ytrain contains value of volumes to be predicted at gievn past and future figures

#OUTPUT
#optimizers and loss declaration
#compiling model



def openForecast(stock , model , nFut):
    dates = list(stock['Date']) #getting dates off the dataframe (stock data)
    dates = [dt.datetime.strptime(date, '%Y-%m-%d').date() for date in dates] #converting dates to timestamps

    ## creating dataset of chosen features to work ahead with LSTM-model
    features = list(stock)[1:-1]
    data = stock[features]
    ft = data.columns.values
    # st.write("The features selected to train the model are : \n [ " , ft[0] , ft[1] , ft[2] , ft[3] , " ]")

    ##DATA PRE-PROCESSING:
    data = data.astype(float)
    dataset = data.values

    #feature scaling:
    ##for input data
    sc = StandardScaler()
    sc_dataset = sc.fit_transform(dataset)
    #for output data
    pred_sc = StandardScaler()
    pred_sc.fit(dataset[:, 0:1 ])

    # INPUT-OUTPUT SPLIT FOR TIME SERIES ANALYSIS
    Xtrain = [] #trend to be analyzed
    ytrain = [] #output for the given-trend
    nFuture = 1 #60 #7 #30   # Number of days we want top predict into the future
    nPast = 14 #90 #30 #100     # Number of past days we want to use to predict the future

    rows = data.shape[0]
    cols = data.shape[1]
    for i in range(nPast ,  rows - nFuture +1):
        Xtrain.append(sc_dataset[i - nPast : i , 0:cols])
        ytrain.append(sc_dataset[i + nFuture - 1 : i + nFuture , 0])
    Xtrain = np.array(Xtrain)
    ytrain = np.array(ytrain)
    # FUTURE FORECAST:
    #GENERATING DATE SEQUENCES FOR FUTURE
    futureDates = pd.date_range(dates[-1], periods=nFut, freq='1d').tolist()
    futureDatesList = []
    for i in futureDates:
        futureDatesList.append(i.date())
    def to_Timestamp(x):
        return dt.datetime.strptime(x.strftime('%Y%m%d'), '%Y%m%d')
    #MODEL PREDICTIONS
    futurePreds = model.predict(Xtrain[-nFut:])
    trainPreds = model.predict(Xtrain[nPast:])
    #INVERSE SCALING
    y_predFuture = pred_sc.inverse_transform(futurePreds)
    y_predTrain = pred_sc.inverse_transform(trainPreds)
    #ARRANGING STUFF
    FUT_PREDS = pd.DataFrame(y_predFuture, columns=["Open"]).set_index(pd.Series(futureDatesList))
    TRAIN_PREDS = pd.DataFrame(y_predTrain, columns=["Open"]).set_index(pd.Series(dates[2 * nPast + nFuture - 1:]))
    TRAIN_PREDS.index = TRAIN_PREDS.index.to_series().apply(to_Timestamp)
    trainSet = pd.DataFrame(data, columns=features)
    trainSet.index = dates
    trainSet.index = pd.to_datetime(trainSet.index)
    return FUT_PREDS , TRAIN_PREDS , futureDatesList , trainSet