import pandas as pd
import numpy as np
import datetime as dt
from sklearn.preprocessing import StandardScaler
import keras
import cufflinks as cf
cf.go_offline()

# stockv = pd.read_csv("../data/meb.csv")

# model1 = keras.models.load_model("../forecast/models/model1.h5")

def to_Timestamp(x):
    return dt.datetime.strptime(x.strftime('%Y%m%d'), '%Y%m%d')


def volumeForecast(stockv , model1 , nFutForV):
    # stockV = pd.read_csv("meb.csv")
    datesForV = list(stockv['Date'])
    datesForV = [dt.datetime.strptime(date, '%Y-%m-%d').date() for date in datesForV]


    featuresForV = list(stockv)[1:]
    dataForV = stockv[featuresForV]
    dataForV = dataForV.astype(float)
    datasetForV = dataForV.values

    print(dataForV.columns)

    scForV = StandardScaler()
    sc_datasetForV = scForV.fit_transform(datasetForV)
    pred_scForV = StandardScaler()
    pred_scForV.fit_transform(datasetForV[:, -1: ]) #for output values

    XtrainForV = [] #trend to be analyzed
    ytrainForV = []

    nFutureForV = 1 #60 #7 #30   # Number of days we want top predict into the future
    nPastForV = 30

    rowsForV = datasetForV.shape[0]
    colsForV = datasetForV.shape[1]
    for i in range(nPastForV ,  rowsForV - nFutureForV +1):
        XtrainForV.append(sc_datasetForV[i - nPastForV : i , 0:colsForV])
        ytrainForV.append(sc_datasetForV[i + nFutureForV - 1 : i + nFutureForV , -1])

    XtrainForV = np.array(XtrainForV)
    ytrainForV = np.array(ytrainForV)


    futureDatesForV = pd.date_range(datesForV[-1], periods=nFutForV, freq='1d').tolist()
    futureDatesListForV = []
    for i in futureDatesForV:
        futureDatesListForV.append(i.date())
    futurePredsForV = model1.predict(XtrainForV[-nFutForV:])
    trainPredsForV = model1.predict(XtrainForV[nPastForV:])

    y_predFutureForV = pred_scForV.inverse_transform(futurePredsForV)
    y_predTrainForV = pred_scForV.inverse_transform(trainPredsForV)

    FUT_PREDSforV = pd.DataFrame(y_predFutureForV, columns=["Volume"]).set_index(pd.Series(futureDatesListForV))
    TRAIN_PREDSforV = pd.DataFrame(y_predTrainForV, columns=["Volume"]).set_index(pd.Series(datesForV[2 * nPastForV + nFutureForV - 1:]))

    TRAIN_PREDSforV.index = TRAIN_PREDSforV.index.to_series().apply(to_Timestamp)

    trainSetForV = pd.DataFrame(dataForV, columns=featuresForV)
    trainSetForV.index = datesForV
    trainSetForV.index = pd.to_datetime(trainSetForV.index)

    return FUT_PREDSforV , TRAIN_PREDSforV , futureDatesListForV , trainSetForV