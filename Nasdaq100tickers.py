# CS5010 Project


from bs4 import BeautifulSoup
import urllib
import re

def getTickers():
    
    page = urllib.request.urlopen("http://www.cnbc.com/nasdaq-100/")
    
    soup= BeautifulSoup(page,"html.parser")
    
    # tickers
    sites=[]
    for link in soup.find_all('a'):
        sites.append(link.get('href'))
    
    #for line in sites:
    #    print(line)    
        #if line[0:28]==str("http://data.cnbc.com/quotes/"):
        #    print(line)
    
    pat=re.compile("http://data.cnbc.com/quotes/")
    
    # Using regular expressions we gather all the companies listed in the 
    # Nasdaq100 and we extract the tickers
    
    global tickers    
    
    tickers=[]
    for line in sites:
        if pat.match(str(line))!= None:
            tickers.append(line[28:])
    
    return(tickers)
    # Using these tickers and the url from Yahoo Finance
    # We create a list of Yahoo Finance Websites for all
    # the tickers we collected above
    #yahoo_sites=[]
    
    #for i in tickers:
    #    yahoo_sites.append("http://finance.yahoo.com/q?s=" + i)
    
    #print(yahoo_sites)

if __name__=="__main__":
    getTickers()



