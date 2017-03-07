#CS5010

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import os
import numpy as np
import csv

#location = "~\CS5010\Project"

class email:    
    def sendEmail(self,ticker,location,toemail):
        print("\n\nSending email to: "+toemail)
        os.chdir(location)
        #username=input("Type in your Gmail address (********@gmail.com) here: ")
        #password=input("Type in the password: ")
        
        me = "##################" #sender's email address
        you = toemail # recipient's email address
        username =  "##################"
        password = "######'
        
        # Create an instance of the class MIMEMultipart which contains all of the contents of the email
        # - the MIME type can be multipart or alternative.
        msg = MIMEMultipart('multipart') #this main instance contains all of the other sub-instances
        msg['Subject'] = "Stock Price Analysis for: "+str(ticker) #Title (subject) of the email
        msg['From'] = me
        msg['To'] = you
        
        # Read the articles from csv
        article_links=[]
        article_titles=[]
        with open("articles.csv","r",newline="") as csvfile:
            lines = csv.reader(csvfile, delimiter=',', quotechar='\"')
            for line in lines:
                # list of links corresponding to each title, will be used in the hyperlinks
                article_links.append(line[1])
                article_titles.append(line[4])
        
        #Read the Press Releases from csv        
        press_links=[]
        press_titles=[]
        with open("PressReleases.csv","r",newline="") as csvfile:
            lines = csv.reader(csvfile, delimiter=',', quotechar='\"')
            for line in lines:
                # list of links corresponding to each title, will be used in the hyperlinks
                press_links.append(line[1])
                press_titles.append(line[3])
                
        
        '''Create the body of the email (the HTML scripts).'''
        #Start HTML doc
        html="""
             <!DOCTYPE html>
             <html>
             <head>
             </head>
             <body>
             """
        
        #Headline for Press Releases
        headline="""<p style="font-size:20px; line-height:40px">
                    <b><i>Here are the press releases for: """+ticker+"""</i></b>
                    </p>"""
        html+=headline
        
        #Convert Press Release content to HTML format
        html+="""<p style="font-size:14px; line-height:25px">"""
        for i in range(1,10):
            try:
                #use triple quotation marks for the string which is to be converted into html format
                html+="""           
                     {0}<a href=\"{1}\">{2}</a><br>
                     """.format(str(i)+". ",press_links[i],press_titles[i])
            except IndexError: #in case the .csv file which contains less than 5 press release articles 
                break
        
        #Headline for Articles
        headline="""<p style="font-size:20px; line-height:40px">
                    <b><i>You might also want to refer to following related articles: """+ticker+"""</i></b>
                    </p>"""
        html+=headline
        
        #Convert Article content to HTML format
        html+="""<p style="font-size:14px; line-height:25px">"""
        for i in range(1,10):
            try:
                #use triple quotation marks for the string which is to be converted into html format
                html+="""           
                     {0}<a href=\"{1}\">{2}</a><br>
                     """.format(str(i)+". ",article_links[i],article_titles[i])
            except IndexError: #in case the .csv file which contains less than 5 press release articles 
                break
        
        #End HTML doc
        html+="""
              </p>
              </body>
              </html>
              """
        msg_sub = MIMEMultipart('alternative') #creat a sub-instance which contains one line of texts
        msg.attach(msg_sub) #attach this sub-instance to the main instance msg
        msg_sub.attach(MIMEText(html, 'html')) #attach the html text to the sub-instance
        
        ################ Reading and Embedding Bolliger Plot Image
        #Embed an image in the email body
        # Open the image file saved in previous steps, and bind it to a variable (Image)
        fp = open('bband.png', 'rb')
        Image = MIMEImage(fp.read())
        fp.close()
        
        msg_img = MIMEMultipart('alternative') #this instance is also a sub-instance of msg; it will contain the image and its title
        msg.attach(msg_img) #attach this image sub-instance to the main instance
        
        title_text="""
                   <p style="font-size:20px; line-height:40px; color:black">
                   <b><i>Bollinger Plot for: """+ticker+"""</i></b><br>
                   <img src="cid:image1">
                   </p>
                   """
        image_title = MIMEText(title_text, 'html')
        msg_img.attach(image_title) #attach image title to the sub-instance
        
        #assign the Content-ID "image1" to the Image, which will map it to the html code in the image_title ("cid:image1")
        Image.add_header("Content-ID","<image1>") 
        msg_img.attach(Image) #attach the actual Image to the sub-instance
        
        
        #################### Reading and embedding 3d image
        #Embed an image in the email body
        # Open the image file saved in previous steps, and bind it to a variable (Image)
        fp = open('3d.png', 'rb')
        threeD = MIMEImage(fp.read())
        fp.close()
        
        msg_img2 = MIMEMultipart('alternative') #this instance is also a sub-instance of msg; it will contain the image and its title
        msg.attach(msg_img2) #attach this image sub-instance to the main instance
        
        title_text="""
                   <p style="font-size:20px; line-height:40px; color:black">
                   <b><i>3D: Volatality Vs Volume for: """+ticker+"""</i></b><br>
                   <img src="cid:image2">
                   </p>
                   """
        image_title = MIMEText(title_text, 'html')
        msg_img2.attach(image_title) #attach image title to the sub-instance
        
        #assign the Content-ID "image1" to the Image, which will map it to the html code in the image_title ("cid:image1")
        threeD.add_header("Content-ID","<image2>") 
        msg_img2.attach(threeD) #attach the actual Image to the sub-instance
        
        #################### Reading and embedding CandleStick image
        #Embed an image in the email body
        # Open the image file saved in previous steps, and bind it to a variable (Image)
        fp = open('candlestick.png', 'rb')
        cstick = MIMEImage(fp.read())
        fp.close()
        
        msg_img3 = MIMEMultipart('alternative') #this instance is also a sub-instance of msg; it will contain the image and its title
        msg.attach(msg_img3) #attach this image sub-instance to the main instance
        
        title_text="""
                   <p style="font-size:20px; line-height:40px; color:black">
                   <b><i>Daily Price Movement(Candlestick) for: """+ticker+"""</i></b><br>
                   <img src="cid:image3">
                   </p>
                   """
        image_title = MIMEText(title_text, 'html')
        msg_img3.attach(image_title) #attach image title to the sub-instance
        
        #assign the Content-ID "image1" to the Image, which will map it to the html code in the image_title ("cid:image1")
        cstick.add_header("Content-ID","<image3>") 
        msg_img3.attach(cstick) #attach the actual Image to the sub-instance
        
        
        # msg_sub=MIMEMultipart('alternative')
        # msg.attach(msg_sub)
        
        # additional_notes="""<p>***Please check the attachment for the interactive version of the above graph.</p>"""
        # msg_sub.attach(MIMEText(additional_notes,'html'))
        
        # import codecs
        # 
        # bokeh_image = codecs.open('Bokeh_image.html', 'r','utf-8')
        # html_image=bokeh_image.read()
        # bokeh_image.close()
        # 
        # attachment=MIMEText(html_image,'html')
        # attachment.add_header('Content-Disposition', 'attachment; filename="Bokeh_image.html"')
        # msg.attach(attachment)
        
        # Send the email message via SMTP server of Gmail (587 is the unique code for Gmail).
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        
        mail.ehlo()
        mail.starttls()
        
        mail.login(username,password)
        
        mail.sendmail(me, you, msg.as_string())
            
        mail.quit()
        print("\nDone.")