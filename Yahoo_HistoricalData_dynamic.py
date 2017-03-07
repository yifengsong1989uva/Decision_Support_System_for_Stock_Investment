# CS5010 Project


import importlib
import urllib
import codecs
import csv
import os

import numpy as np
import pandas as pd
import pandas.io.data

import datetime
from astropy.constants.si import alpha
time = importlib.import_module('time')

class HistoricDynamic:
        
    def storeResultsCsv(self,df,location):
        os.chdir(location)
        df.to_csv("stock_historic.csv")
        print("\n\nCreated file named stock_historic.csv to "+str(location))
        
    def getFinanceData(self,ticker,date):
        #ticker = "AAPL"
        #ticker information and dates as entered by user is used to fetch the data
        print("\n\nExtracting data from Yahoo Finance Pages")
        url="http://real-chart.finance.yahoo.com/table.csv?s="+ticker+"&a=11&b=12&c=1981&d=07&e=6&f=2015&g=d&ignore=.csv"    
        response = urllib.request.urlopen(url)
        csvfile = csv.reader(codecs.iterdecode(response, 'utf-8'))
         
        csvData=[]
        for line in csvfile:
            csvData.append(line)
         
        headers=csvData[0]
        headers[6] = 'Adj_Close'
        print("\n\n Data Obtained for "+ str(headers))
         
        tableData=[]
        for i in range(len(csvData)-1,0,-1):
            tableData.append(csvData[i])
         
        indexDates=[]
        for i in range(0,len(tableData)):
            s=str(tableData[i][0])
            t=time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d").timetuple())
            indexDates.append(time.asctime(time.localtime(t)))
         
        df = pd.DataFrame(tableData,columns=headers)
        df=df.convert_objects(convert_numeric=True)
        
        print("\n\nPutting data into Pandas Data Frame") 
       
        df.Date=indexDates
         
        df.index=pd.to_datetime(df.Date)
        df.index
        df.pop('Date')
         
        #df['2015-02']
         
        close2015 = df.Close['2015']
        close2015.shift(1)/close2015 - 1
         
        close = close2015.head(5)
        df['MAvg'] = pd.rolling_mean(df.Adj_Close,30)
        df['SDev'] = pd.rolling_std(df.Adj_Close,30)
        df['lower_band'] = df.MAvg - 2*df.SDev
        df['upper_band'] = df.MAvg + 2*df.SDev
        df['alert'] = np.where((df.Adj_Close > df.upper_band) | (df.Adj_Close < df.lower_band), True,False)
        
        print("\n\nDataFrame: ")
        print(df.info())
        
        print("\n\nPrinting last 5 records: ")
        print(df.tail(5))
        
        return df


