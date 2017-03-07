# CS5010 Project


from pylab import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc
from matplotlib import style
import matplotlib.animation as animation
import os
import time
from mpl_toolkits.mplot3d import axes3d, Axes3D

class GraphicPlots:
        ##### Bollinger band ####
    def bollingerBand(self,df,ticker,location):
        print("Rendering Bollinger Plot.....")
        time.sleep(2)
        
        os.chdir(location)
        rows = range(30,500)
        
        #def graph_stock (df):
        fig = plt.figure(num = None, 
                         figsize=(14, 10), 
                         dpi=80, 
                         facecolor='w', 
                         edgecolor='k')
        ax1 = plt.subplot2grid((1,1),(0,0))
        #candlestick_ohlc(ax1, ohlc, width = 0.4, colorup='#008000', colordown='#f9105e')
        
        ax1.plot_date(df.index.values[rows], 
                      df.ix[rows].Adj_Close,'-', 
                      label = 'Adj Close Price', 
                      color = 'c')
        ax1.plot(df.index.values[rows], 
                 df.ix[rows].MAvg, 
                 color = '0.40', 
                 linestyle = '-',
                 label = 'Moving Avg')
        ax1.plot(df.index.values[rows], 
                 df.ix[rows].lower_band, 
                 color = 'blue', 
                 linestyle = '-',
                 label = 'Bollinger Lower')
        ax1.plot(df.index.values[rows], 
                 df.ix[rows].upper_band,
                 color = 'blue', 
                 linestyle = '-',
                 label = 'Bollinger Upper')
        
        #ax1.axhline(0.5, color='k', linewidth = 1)
        
        ax1.fill_between(
                         df.index.values[rows], 
                         df.ix[rows].lower_band, 
                         df.ix[rows].upper_band,
                         facecolor = 'y', 
                         alpha=0.1) 
        
        ax1.fill_between(
                         df.index.values[rows], 
                         df.ix[rows].Adj_Close, 
                         df.ix[rows].lower_band, 
                         where = (df.ix[rows].Adj_Close < df.ix[rows].lower_band),
                         facecolor = 'r', 
                         alpha=0.9) 
        ax1.fill_between(
                         df.index.values[rows], 
                         df.ix[rows].Adj_Close, 
                         df.ix[rows].upper_band, 
                         where = (df.ix[rows].Adj_Close > df.ix[rows].upper_band),
                         facecolor = 'r', 
                         alpha=0.9) 
        for label in ax1.xaxis.get_ticklabels():
            label.set_rotation(45)
        
        ax1.grid(True)
        ax1.xaxis.label.set_color('#4f5458')
        ax1.yaxis.label.set_color('#4f5458')
        ax1.set_yticks([0,0.25,0.5,0.75,1])
        ax1.tick_params(axis='x', colors = '#4f5458')
        ax1.tick_params(axis='y', colors = '#4f5458') 
        
        ax1.spines['left'].set_color('k')
        ax1.spines['left'].set_linewidth(2)
        ax1.spines['bottom'].set_color('k')
        ax1.spines['bottom'].set_linewidth(2)
        ax1.spines['right'].set_visible(False)
        ax1.spines['top'].set_visible(False)
        
        plt.xlabel('Date',fontweight='bold',fontsize=12)
        plt.ylabel('Adjusted Close Price',fontweight='bold',fontsize=12)
        plt.title("Stock Price Movement For :"+ticker, fontweight='bold',fontsize=16, color='#4f5458')
        plt.legend()
        plt.subplots_adjust(left=0.09, bottom=0.2, right=0.94, top=0.9, wspace = 0.2, hspace = 0.1)
        plt.show()
        #savefig('bband.jpg')
        #plt.savefig("bband.png")
        #fig.saveas("bband.png")

#### 3D Plot
############################

    def threeD(self,df,ticker,location):
        print("Rendering 3-D Plot for Volume vs Volatality vs Date.....")
        rows = range(30,500)
        df['Volatality'] = df.High - df.Low
        fig = plt.figure(num = None, 
                         figsize=(14, 10), 
                         dpi=80, 
                         facecolor='w', 
                         edgecolor='k')
        ax = Axes3D(fig)
        #ax = fig.add_subplot(111, projection='3d')
        c = 'r'
        m = 'x'
        xs = np.int32(mdates.date2num(df.index[rows].to_pydatetime()))
        ys = np.int32(df.ix[rows].Volatality)
        zs = np.int32(df.ix[rows].Volume)
        
        # xs = mdates.date2num(df.index[rows].to_pydatetime())
        # ys = df.ix[rows].Volatality
        # zs = df.ix[rows].Volume
        
        ax.scatter(xs, ys, zs, c=c, marker=m)
        ax.set_xlabel('Date')
        ax.set_ylabel('Volatality/Day')
        ax.set_zlabel('Volume')
        plt.title('3D graph of Date vs Volatality vs Volume', fontweight = 'bold', fontsize = '13')
        plt.show()

### Candlestick graph
################################

    def CandlestickGraph(self,df,ticker,location):
        print("Rendering Candlestick plot.....")
        rows = range(30,5000)
        ohlc = []
        for i in rows:
            r = (mdates.date2num(df.index[i].to_pydatetime()),
                 df.ix[i].Open,
                 df.ix[i].Close,
                 df.ix[i].High,
                 df.ix[i].Low)
            ohlc.append(r)
        fig = plt.figure(num = None, 
                         figsize=(14, 10), 
                         dpi=80, 
                         facecolor='w', 
                         edgecolor='k')
        ax1 = plt.subplot2grid((1,1),(0,0))
        candlestick_ohlc(ax1, ohlc, width = 0.8, colorup='g', colordown='r')
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        #ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.title("Candlestick plot for Stock Price:"+ticker)
        plt.subplots_adjust(left=0.09, bottom=0.2, right=0.94, top=0.9, wspace = 0.2, hspace = 0.1)
        plt.show()
