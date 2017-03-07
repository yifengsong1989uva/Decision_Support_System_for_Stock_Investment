# CS5010 Project


from bs4 import BeautifulSoup
import urllib
import pandas as pd
import re
from datetime import datetime, date, timedelta
from Nasdaq100tickers import getTickers
import os

class SourceArticles:
    def ScrapeArticles(self,ticker,location):
        os.chdir(location)
        print("\n\nPulling Articles from website....\n\n")
        # Get tickers from "Nasdaq100tickers1" module
        #tickers=[]
        #tickers=getTickers()
        
        # Start-Positon for Lists Capturing Web Data
        start_i=0
        # Initiate Lists
        articleHref=[]
        articleTitle=[]
        publisher=[]
        articleDate=[]
        ticker1=[]
    
        # Set initial date for webcrawling
        # Today minus 60 days
        t=20
        for i in range(t,0,-1):
            i_date=i*-1
            initialDate = date.today() + timedelta(days=i_date)
            str_initialDate=str(initialDate.strftime('%Y-%m-%d'))
            url="http://finance.yahoo.com/q/h?s="+ticker+"&t="+str_initialDate+""
            response=urllib.request.urlopen(url)
            soup=BeautifulSoup(response,"html.parser")
            
            # Increase t by 1 for the next iteration after the round of scraping
            #t=t+1
            
            # Get Article Hyperlink References and Article Titles
            for i in soup.find_all(href=re.compile("\/finance\/external\/")):
                articleTitle.append(i.get_text())
                articleHref.append(i.get("href"))               
            
            # Get Article Publishers and Article Dates
            for i in soup.find_all(class_="mod yfi_quote_headline withsky"):
                for d in i.find_all("ul"):
                    for j in d.find_all("li"):
                        for z in j.find_all("a"):
                            if z.get("href")[0:31]==str("http://us.rd.yahoo.com/finance/"):
                                for k in j.find_all("cite"):
                                    publisher.append(str(k.get_text().split("\xa0")[0]))
                                    articleDate.append(str(k.parent.parent.previous_sibling.get_text()))
            
            # Publishers may contain "at " preciding the publisher name 
            # We remove the "at " if it exists
            for i in range(start_i,len(publisher)):
                if publisher[i][0:2]=="at":
                    publisher[i]=publisher[i][3:]
                else:
                    publisher[i]=publisher[i]
            
            # Need to covert scraped date string into usable format
            for i in range(start_i,len(articleDate)):
                i_replace=str(articleDate[i]).replace(" ","-")
                i_tuple=i_replace.split(",")
                articleDate[i]=str(i_tuple[1]+i_tuple[2])[1:]
            
            # Converted Date String is converted into format to use for indexing the DataFrame
            for i in range(start_i,len(articleDate)):
                articleDate[i]=datetime.strptime(str(articleDate[i]),"%B-%d-%Y")
            
            # How many new articles were added to the lists
            num_articles=len(articleDate)-start_i        
            
            # create start points "start_i" for next set of articles        
            start_i=len(articleDate) 
                    
            # Create list of tickers relevant to this set of articles
            for i in range(0,num_articles):
                ticker1.append(ticker)
    
            # Check to ensure program is running smoothly
            len_d=len(articleDate)
            len_titl=len(articleTitle)
            len_href=len(articleHref)
            len_pub=len(publisher)
            len_tick=len(ticker1)
            
            if len_d==len_titl and len_d==len_href and len_d==len_pub and len_d==len_tick:
                print("Articles for "+str(t)+" Days: "+str(i_date))
    
        # store completed lists to dataframe
        df = pd.DataFrame({'Title' : articleTitle,
                      'Link':articleHref,
                      'Publisher': publisher,
                      'articleDate':articleDate,
                      'Ticker': ticker1}
                     )
        # set index of dataframe to date
        df = df.set_index(df.articleDate)
        df.pop('articleDate')
        
        # create subset that will be used to drop dubplicate articles
        dup_subset=['Ticker','Title']
        
        # Drop Duplicates
        df.drop_duplicates(subset=dup_subset, take_last=True, inplace=True)
        
        # Store dataFrame to variable
        articlesDataFrame = df
        
        # Output DataFrame to .csv file
        articlesDataFrame.to_csv("articles.csv", sep=",")
        print("Articles saved as csv to working directory")
