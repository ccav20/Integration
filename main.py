
import numpy as np
import pandas as pd
from sendgmailauto import sendEmail
from LinkedInScraping_master import utils as ut
from linkedinintegration import integration
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from lnk_to_lusha import *



df = pd.read_excel("test 2.xlsx")
print(df['Linkedin'])

#LinkedIn/Lusha Integration
df = integration(df)

#sending info to excel
df.to_excel("test.xlsx", index=False)

#sending email
sendEmail(df)


