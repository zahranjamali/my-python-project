import requests
import smtplib
import os
import paramiko #for ssh'ing
import linode_api4
import schedule

EMAIL_ADDRESS = os.environ.get('EMAIL_ADR') #give any name to env variable..set it on pycharm
EMAIL_PASSWORD = os.environ.get('EMAIL_PWD') #<token from app password>
LINODE_CLIENT = os.environ.get('LINODE_TOKEN') #token from api token from linode

def send_notification (email_msg):
    print('Sending an email...')
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()  # Ensuring security
        smtp.ehlo()  # Identifies the email app with python
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # allow less secure app ON and create app password in gmail
        msg = f"Subject: SITE DOWN \n {email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, msg)

def restart_container():
    print('Restarting the Application...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='139.64.5.54',port=80, username='root', key_filename='/home/zahran/.ssh/id_rsa')
    stdin, stdout, stderr = ssh.exec_command('docker start c342kljflakfj')
    print(stdout.readline())
    ssh.close()

def restart_server_and_container():

def monitor_application():
    try:
        response = requests.get('https://nginxserver.com') #give your respective server add
        if response.status_code == 200:
            print('Application is working')
        else:
            print('Application is not working')
            msg = f"Application return {response.status_code} fix the issue!."
            send_notification(msg)
            #restarting the application
            restart_container()
    except Exception as ex:
        print(f'Connection error happened: {ex}')
        msg = "Application not accessable at all fix the issue!."
        send_notification(msg)
        restart_server_and_container()


schedule.every(5).minutes.do(monitor_application)

while True:
    schedule.run_pending()