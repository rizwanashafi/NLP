# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib 

import os  
import pickle

# Creating utils for Gmail APIs  
from googleapiclient.discovery import build  
from google_auth_oauthlib.flow import InstalledAppFlow  
from google.auth.transport.requests import Request 

# Importing libraries for encoding/decoding messages in base64  
from base64 import urlsafe_b64decode, urlsafe_b64encode 
# Importing libraries for dealing with the attachment of MIME types in Gmail  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  
from email.mime.image import MIMEImage  
from email.mime.audio import MIMEAudio  
from email.mime.base import MIMEBase  
from email.mime.multipart import MIMEMultipart  
from mimetypes import guess_type as guess_mime_type

# Request all access from Gmail APIs and project  
SCOPES = 'https://mail.google.com/'
OurEmailID = 'rizwanashafi744@gmail.com' # giving our Gmail Id

# using a default function to authenticate Gmail APIs  
def authenticateGmailAPIs():  
    creds = None  
    # Authorizing the Gmail APIs with tokens of pickles  
    if os.path.exists("token.pickle"): # using if else statement  
        with open("token.pickle", "rb") as token:  
            creds = pickle.load(token)

 # If there are no valid credentials available in device, we will let the user sign in manually  
    if not creds or not creds.valid:  
        if creds and creds.expired and creds.refresh_token:  
            creds.refresh(Request())  
        else:  
            flow = InstalledAppFlow.from_client_secrets_file('C:/Users/new gen/Documents/python project/client_secret_999515627859-q0eb5q6cd8pie26tmivj9dctuulj18gb.apps.googleusercontent.com.json', SCOPES) # downloaded credential name  
            creds = flow.run_local_server(port=0) # running credentials  
        # Save the credentials for the next run  
        with open("token.pickle", "wb") as token:  
            pickle.dump(creds, token)  
    return build('Gmail', 'v1', credentials=creds) # using Gmail to authenticate  
  
# Get the Gmail API service by calling the function  
service = authenticateGmailAPIs()

 
  
# Using a default funnction to add attachments in Mail  
def AddAttachment(mail, NameofFile):  
    content_type, encoding = guess_mime_type(NameofFile)  
    if content_type is None or encoding is not None: # defining none file type attachment  
        content_type = 'application/octet-stream'  
    main_type, sub_type = content_type.split('/', 1)  
    if main_type == 'text': # defining text file type attachment  
        fp = open(NameofFile, 'rb') # opening file  
        msg = MIMEText(fp.read().decode(), _subtype = sub_type)  
        fp.close()   
    elif main_type == 'image': # defining image file type attachment  
        fp = open(NameofFile, 'rb')  
        msg = MIMEImage(fp.read(), _subtype = sub_type)  
        fp.close()  
    elif main_type == 'audio': # defining audio file type attachment  
        fp = open(NameofFile, 'rb')  
        msg = MIMEAudio(fp.read(), _subtype = sub_type) # reading file  
        fp.close()  
    else:  
        fp = open(NameofFile, 'rb')  
        msg = MIMEBase(main_type, sub_type)  
        msg.set_payload(fp.read())  
        fp.close() # closing file  
    NameofFile = os.path.basename(NameofFile)  
    msg.add_header('Content-Disposition', 'attachment', NameofFile = NameofFile)  
    mail.attach(msg) # composing the mail with given attachment  
  
# Creating mail with a default function  
def CreateMail(RecieverMail, SubofMail, BodyofMail, attachments=[]): # various import content of mail as function's parameter  
    # Using if else to check if there is any attachment in mail or not  
    if not attachments: # no attachment is given in the mail  
        mail = MIMEText(BodyofMail) # Body of Mail  
        mail['to'] = RecieverMail # mail ID of Reciever  
        mail['from'] = OurEmailID # our mail ID  
        mail['subject'] = SubofMail # Subject of Mail  
    else: # attachment is given in the mail  
        mail = MIMEMultipart()  
        mail['to'] = RecieverMail  
        mail['from'] = OurEmailID  
        mail['subject'] = SubofMail  
        mail.attach(MIMEText(BodyofMail))  
        for NameofFile in attachments:  
            AddAttachment(mail, NameofFile)  
    return {'raw': urlsafe_b64encode(mail.as_bytes()).decode()}  
  
# Creating a default function to send a mail  
def SendMail(ServicesGA, RecieverMail, SubofMail, BodyofMail, attachments=[]):  
    return ServicesGA.users().messages().send(  
      userId = "me",  
      body = CreateMail(RecieverMail, SubofMail, BodyofMail, attachments)  
    ).execute() # Body of the mail with execute() function  
  
# Sending an email by adding important content, i.e., Reciever's mail, Subject, Body, etc.  
SendMail(service, "rizwana0033@gmail.com", "Python Project i.e., This is the subject of Mail we are sendimg!",   
            "Now, this is the body of the email we are writing and we can add only written text here!", ["C:/Users/new gen/Documents/python project/test.txt", "C:/Users/new gen/Documents/python project/client_secret_999515627859-q0eb5q6cd8pie26tmivj9dctuulj18gb.apps.googleusercontent.com.json"]) # calling out default SendMail() function  