import requests
import smtplib
import os

EMAIL_ADDRESS = os.environ.get('EMAIL_ADR') #give any name to env variable..set it on pycharm
EMAIL_PASSWORD = os.environ.get('EMAIL_PWD') #<token from app password>

def send_notification (email_msg)
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()  # Ensuring security
        smtp.ehlo()  # Identifies the email app with python
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # allow less secure app ON and create app password in gmail
        msg = f"Subject: SITE DOWN \n {email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, msg)

try:
    response = requests.get('https://nginxserver.com') #give your respective server add
    if response.status_code == 200:
        print('Application is working')
    else:
        print('Application is not working')
        msg = f"Application return {response.status_code} fix the issue!."
        send_notification(msg)
except Exception as ex:
    msg = "Application not accessable at all fix the issue!."
    send_notification(msg)
