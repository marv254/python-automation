import boto3
import requests
import smtplib
import os

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")


def send_notification(email_msg):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f"Subject: SITE DOWN\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, "devopsmarv@gmail.com", message)


try:
    response = requests.get('http://ec2-13-245-80-251.af-south-1.compute.amazonaws.com:8080/')
    if response.status_code == 200:
        print('Application is running successfully')
    else:
        print('Application Down. Fix it')
        # send email
        msg = f"Application returned {response.status_code}. Fix the issue ! Restart the Application "
        send_notification(msg)
except Exception as ex:
    print(f"Connection error happened: {ex}")
    # send email
    msg = f"Application not accessible at all. Fix the issue ! Restart the Application"
    send_notification(msg)
