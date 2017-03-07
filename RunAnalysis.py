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

from pylab import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc
from matplotlib import style
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import axes3d, Axes3D

#import ScrapeYahooPressRelease
from Yahoo_HistoricalData_dynamic import HistoricDynamic
from GraphicPlots import GraphicPlots
from ScrapeYahooArticles import SourceArticles
from ScrapeYahooPressRelease import PressRelease
from EmailReport import email
 
#Set Working Directory
location = "~\CS5010\Project"

#User Input Module
class runAnalysis:
    def __init__(self,userName, emailID, ticker, dt):
        self.ticker = ticker
        self.emailID = emailID
        self.userName = userName
        self.dt = dt
    def createReport(self):
        df = HistoricDynamic().getFinanceData(self.ticker,self.dt)
         
        input("\n\nPress Enter to Store Results to CSV...")
        HistoricDynamic().storeResultsCsv(df,location)
         
        input("\n\nPress Enter to Create Graphic Plots...")
        GraphicPlots().bollingerBand(df,self.ticker,location)
        GraphicPlots().threeD(df,self.ticker,location)
        GraphicPlots().CandlestickGraph(df,self.ticker,location)
        
        input("\n\nPress Enter to Send the email right away...")
        SourceArticles().ScrapeArticles(self.ticker,location)
        PressRelease().scrapePressRelease(self.ticker,location)
        email().sendEmail(self.ticker,location,self.emailID)

userName = input("Please enter your User Name: ")
print("User Name: "+userName)
emailID = input("Enter your email ID: ")
print("Email ID: "+userName)
ticker = input("Enter the stock ticker: ")
print("Ticker: "+ ticker)
dt = input("Enter the date (MM-DD-YYYY): ")
print("Date entered is :"+dt)

# userName = '######'
# emailID="##################"
# ticker = 'AAPL'
# dt = '12-12-2014'

run = runAnalysis(userName, emailID, ticker, dt)
run.createReport()


