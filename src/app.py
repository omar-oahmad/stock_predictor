import keras.models
import pandas as pd
import streamlit as st
import cufflinks as cf
import plotly.express as px
import datetime
# init_notebook_mode(connected=True)
from forecast.open.open import openForecast
from forecast.volume.volume import volumeForecast
cf.go_offline()
import plotly.graph_objects as go

st.set_page_config(page_title= "Stock Insight" , layout="wide" )

title_temp = """
<div style="background-color:{};padding:10px;border-radius:10px">
<h1 style="color:{};text-align:center;">{}</h1>
</div>
"""
sub_title_temp = """
<div style="background-color:{};padding:0.5px;border-radius:5px;">
<h4 style="color:{};text-align:center;">{}</h6>
</div>
"""
head_title_temp = """<h6 style="text-align:left;margin-top:2px">{}</h6>"""

st.markdown(title_temp.format('#1E3231','white' , "STOCK INSIGHT"),unsafe_allow_html=True)
st.write("")
st.write("")

user_in = st.text_input("Enter the company name : " , "MEBL")
stock = pd.read_csv("./data/meb.csv"); #importing dataset
model0 = keras.models.load_model("./forecast/models/model0.h5")
model1 = keras.models.load_model("./forecast/models/model1.h5")

st.markdown(sub_title_temp.format("#646F58" , "white" , user_in+" STOCK FROM 2018 - 2022"),unsafe_allow_html=True)
# st.subheader(user_in , " STOCK FROM 2018 - 2022")
stock_wd_date = stock.set_index("Date")
col1 , col2 = st.columns((1,1.5))
with col1:
    st.markdown(head_title_temp.format("HISTORICAL DATA"),unsafe_allow_html=True)
    fig = go.Figure(
        data = [go.Table (columnorder = [0,1,2,3,4,5], columnwidth = [15,10,10,10,10,10],
                          header = dict(
                              values = list(stock.columns),
                              font=dict(size=12, color = 'white'),
                              fill_color = '#264653',
                              line_color = 'rgba(255,255,255,0.2)',
                              align = ['left','center'],
                              #text wrapping
                              height=40
                          )
                          , cells = dict(
                values = [stock[K].tolist() for K in stock.columns],
                font=dict(size=12 , color = "black"),
                align = ['left','center'],
                line_color = 'rgba(255,255,255,0.2)',
                height=30))])
    fig.update_layout(title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=480)
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.markdown(head_title_temp.format("QUICK SUMMARY"),unsafe_allow_html=True)
    fg = px.line(x=stock["Date"], y=stock["Open"] ,
                 labels={"x" : "Date" , "y":"Open"})
    fg.update_layout(
        xaxis_title="Time",
        yaxis_title="Stock Open Prices",
        width = 750,
        height = 500
    )
    st.plotly_chart(fg)
    # st.subheader("Quick Summary")
    # st.line_chart(stock["Open"] , use_container_width=True , height= 300 , width= 600 ,)
cal1, em1, emp2, emp3  = st.columns((2,1,1,1))
d = "2018-01-02";
with cal1:
    ch_d = st.date_input(" Choose Day:",datetime.date(2018, 1, 1))
    d = str(ch_d)

m1, m2, m3, m4, m5,m6 = st.columns((1,1,1,1,1.7,1.7))
avb_days = stock_wd_date.index.to_list()
pi = avb_days.index(d) - 1
if(d in stock_wd_date.index.to_list()):
    [o,h,l,c,v] = stock_wd_date.loc[d].tolist()
    [po,ph,pl,pc,pv] = stock_wd_date.iloc[pi].tolist()
else:
    [o,h,l,c,v] = stock_wd_date.loc["2018-01-02"].tolist()
    [po,ph,pl,pc,pv] = stock_wd_date.iloc[1].tolist()
change  = ((c - pc) / pc ) * (100)
ch = str(change.__round__(1)) + "%"

with m1 :
    s = "Open  " + str(o)
    new_title = '<p style="background : #3C6997; height : 100% ;padding : 3px; margin : 10%;color:White; font-size: 25px; text-align : center;border-radius : 5px">'+s+'</p>'
    st.markdown(new_title, unsafe_allow_html=True)
with m2 :
    s = "High  " + str(h)
    new_title = '<p style="background : #3C6997; height : 100%;padding : 3px ; margin : 10%;color:White; font-size: 25px; text-align : center;border-radius : 5px">'+s+'</p>'
    st.markdown(new_title, unsafe_allow_html=True)
with m3 :
    s = "Low " + str(l)
    new_title = '<p style="background : #3C6997; height : 100% ;padding : 3px; margin : 10%;color:White; font-size: 25px; text-align : center;border-radius : 5px">'+s+'</p>'
    st.markdown(new_title, unsafe_allow_html=True)
with m4 :
    s = "Close  " + str(c)
    new_title = '<p style="background : #3C6997; height : 100% ;padding : 2px; margin : 10%;color:White; font-size: 25px; text-align : center;border-radius : 5px">'+s+'</p>'
    st.markdown(new_title, unsafe_allow_html=True)
with m5 :
    s = "Volume  " + str(v)
    new_title = '<p style="background : #5B8C5A; height : 100%;padding : 1px ; margin : 10%;color:White; font-size: 25px; text-align : center;border-radius : 5px">'+s+'</p>'
    st.markdown(new_title, unsafe_allow_html=True)
with m6 :
    s = "Change  " + str(ch)
    new_title = '<p style="background : #92AC86; height : 100% ;padding : 1px; margin : 10%;color:White; font-size: 25px; text-align : center;border-radius : 5px">'+s+'</p>'
    st.markdown(new_title, unsafe_allow_html=True)


st.markdown(sub_title_temp.format("#89B6A5" , "white" , "EXPLORING RELATIONSHIPS AMONG VARIABLES"),unsafe_allow_html=True)
# st.subheader("OPEN RELATIONSHIP")
variables = stock.columns[1:]
choice = st.selectbox('With :', variables, help = 'Filter stock to show relationship with one variable.')
plot1 , plot2 = st.columns((1.5,1))
with plot1:
    st.markdown(head_title_temp.format("TRENDS OVER TIME"),unsafe_allow_html=True)
    fg = go.Figure()
    fg.add_trace(go.Scatter(
        x = stock.index.values,
        y = stock["Open"],
        line=dict(color='gray') , name = 'Open Stock Price'
    ))

    fg.add_trace(go.Scatter(
        x = stock.index.values,
        y = stock[choice],
        line=dict(color='orange') , name =  choice + 'Stock Price'
    ))
    fg.update_layout(
        xaxis_title = "Time", yaxis_title = "Value",
        width = 700, height = 500
    )
    st.plotly_chart(fg)
with plot2:
    st.markdown(head_title_temp.format("OPEN vs. "+choice),unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    fg = px.scatter(stock , x = choice , y = "Open")
    fg.update_layout(
        width = 500, height = 400
    )
    st.plotly_chart(fg)

# st.markdown("<hr/>",unsafe_allow_html=True)


# #  ***********************************************************************************
# #FORECAST:
st.markdown(sub_title_temp.format("#89B6A5" , "white" , "STOCK FORECAST"),unsafe_allow_html=True)
# # st.subheader("STOCK FORECAST")
nFut = 90
opt1 , e1 , e2 = st.columns((1,2,2))
with opt1:
    nDs = st.text_input("Enter the days range to forecast (1-90)" , 90);
    nFut = int(nDs)
# ****************************************************************************
FUT_PREDS , TRAIN_PREDS , futureDatesList , trainSet = openForecast(stock , model0 ,nFut)

chart , visual = st.columns((1,1.5))
with chart:
    st.markdown(head_title_temp.format("CHART VIEW"),unsafe_allow_html=True)
    fut_preds = FUT_PREDS.reset_index()
    fig = go.Figure(
        data = [go.Table (columnorder = [0,1], columnwidth = [15,10],
                          header = dict(
                              values = ["Date" , "Open"],
                              font=dict(size=12, color = 'white'),
                              fill_color = '#264653',
                              line_color = 'rgba(255,255,255,0.2)',
                              align = ['left','center'],
                              #text wrapping
                              height=40
                          )
                          , cells = dict(
                values = [fut_preds[K].tolist() for K in fut_preds.columns],
                font=dict(size=12 , color = "black"),
                align = ['left','center'],
                line_color = 'rgba(255,255,255,0.2)',
                height=30))])
    fig.update_layout(title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=480)
    st.plotly_chart(fig, use_container_width=True)
with visual:
    st.markdown(head_title_temp.format("VISUALS"),unsafe_allow_html=True)
    fig0 = px.line(x=futureDatesList, y=FUT_PREDS["Open"] ,
                   labels={"x" : "Date" , "y":"Open"} ,
                   height = 500 ,width=750)
    fig0.update_layout(
        xaxis_title="Time",
        yaxis_title="OPEN PRICES",
        legend_title="Legend Title",
    )
    st.plotly_chart(fig0)

st.markdown(sub_title_temp.format("#89B6A5" , "white" , "MODEL SUMMARY"),unsafe_allow_html=True)
# st.subheader("FORECASTING MODEL SUMMARY")
#PLOTTING actual vs. predicted
# Plotting
STARTDATE = TRAIN_PREDS.index[0]
# import plotly.graph_objects as go
st.markdown(head_title_temp.format("Predicted vs. Actual"),unsafe_allow_html=True)
fg = go.Figure()
fg.add_trace(go.Scatter(
    x = trainSet.loc[STARTDATE:].index,
    y = trainSet.loc[STARTDATE:]["Open"],
    line=dict(color='blue') , name = 'Actual Stock Price'
))

fg.add_trace(go.Scatter(
    x = FUT_PREDS.index,
    y = FUT_PREDS["Open"],
    line=dict(color='red') , name = 'Future Predicted Price'
))

fg.add_trace(go.Scatter(
    x = TRAIN_PREDS.loc[STARTDATE:].index,
    y = TRAIN_PREDS.loc[STARTDATE:]["Open"],
    line=dict(color='orange'), name = 'Predicted Train Prices'
))
fg.add_vline(x=min(FUT_PREDS.index), line_width=1.5, line_dash="dash", line_color="green")

fg.update_layout(
    xaxis_title="Time",
    yaxis_title="Stock Open Prices",
    height = 500 ,
    width = 1200
)
st.plotly_chart(fg)

# VOLUME FORECAST

st.markdown(sub_title_temp.format("#89B6A5" , "white" , "VOLUME FORECAST"),unsafe_allow_html=True)

nFutForV = 30

opt11 , e11 , e22 = st.columns((1,2,2))
with opt11:
    nDsV = st.text_input("Enter the days range to forecast (1-90)" , 30);
    nFutForV = int(nDsV)

FUT_PREDSforV , TRAIN_PREDSforV , futureDatesListForV , trainSetForV = volumeForecast(stock, model1 , nFutForV)

chartV , visualV = st.columns((1,1.5))
with chartV:
    st.markdown(head_title_temp.format("CHART VIEW"),unsafe_allow_html=True)
    fut_preds = FUT_PREDSforV.reset_index()
    fig = go.Figure(
        data = [go.Table (columnorder = [0,1], columnwidth = [15,10],
                          header = dict(
                              values = ["Date" , "Volume"],
                              font=dict(size=12, color = 'white'),
                              fill_color = '#264653',
                              line_color = 'rgba(255,255,255,0.2)',
                              align = ['left','center'],
                              #text wrapping
                              height=40
                          )
                          , cells = dict(
                values = [fut_preds[K].tolist() for K in fut_preds.columns],
                font=dict(size=12 , color = "black"),
                align = ['left','center'],
                line_color = 'rgba(255,255,255,0.2)',
                height=30))])
    fig.update_layout(title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=480)
    st.plotly_chart(fig, use_container_width=True)
with visualV:
    st.markdown(head_title_temp.format("VISUALS"),unsafe_allow_html=True)
    fig0 = px.line(x=futureDatesListForV, y=FUT_PREDSforV["Volume"] ,
                   labels={"x" : "Date" , "y":"Volume"} ,
                   height = 500 ,width=750)
    fig0.update_layout(
        # title="VISUALS",
        xaxis_title="Time",
        yaxis_title="Volume",
        legend_title="Legend Title",
    )
    st.plotly_chart(fig0)




st.markdown(sub_title_temp.format("#89B6A5" , "white" , "MODEL SUMMARY"),unsafe_allow_html=True)
# st.subheader("FORECASTING MODEL SUMMARY")
#PLOTTING actual vs. predicted
# Plotting
STARTDATE = TRAIN_PREDSforV.index[0]
# import plotly.graph_objects as go
fg0 = go.Figure()
fg0.add_trace(go.Scatter(
    x = trainSetForV.loc[STARTDATE:].index,
    y = trainSetForV.loc[STARTDATE:]["Volume"],
    line=dict(color='blue') , name = 'Actual Volume'
))

fg0.add_trace(go.Scatter(
    x = FUT_PREDSforV.index,
    y = FUT_PREDSforV["Volume"],
    line=dict(color='red') , name = 'Future Predicted Volume'
))

fg0.add_trace(go.Scatter(
    x = TRAIN_PREDSforV.loc[STARTDATE:].index,
    y = TRAIN_PREDSforV.loc[STARTDATE:]["Volume"],
    line=dict(color='orange'), name = 'Predicted Train Volume'
))
fg0.add_vline(x=min(FUT_PREDSforV.index), line_width=1.5, line_dash="dash", line_color="green")

fg0.update_layout(
    title="Pred vs. Actual",
    xaxis_title="Time",
    yaxis_title="Stock Volume",
    height = 500 ,
    width = 1200
)
st.plotly_chart(fg0)