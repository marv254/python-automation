import requests
import smtplib
import os
import paramiko
import linode_api4
import time
import schedule

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
LINODE_TOKEN = os.environ.get('LINODE_TOKEN')


def send_notification(email_msg):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f"Subject: SITE DOWN\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)


def restart_container():
    print('Restarting the container...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect('13.245.13.213', username='ec2-user', key_filename='/home/marv/.ssh/web-server.pem')
    stdin, stdout, stderr, = ssh.exec_command('docker start 0262159d88b2')
    print(stdout.readlines())
    ssh.close()


def restart_server_and_container():
    # restart Linode server
    print("Rebooting the server... ")
    client = linode_api4.linode_client(LINODE_TOKEN)
    nginx_server = client.load(linode_api4.Instance, 24920590)
    nginx_server.reboot()

    # restart the application
    while True:
        nginx_server = client.load(linode_api4.Instance, 24920590)
        if nginx_server.status == 'running':
            time.sleep(5)
            restart_container()
            break


def monitor_application():
    try:
        response = requests.get('http://ec2-13-245-13-213.af-south-1.compute.amazonaws.com:8080/')
        if response.status_code == 200:
            print('Application is running successfully')
        else:
            print('Application Down. Fix it')
            # send email
            msg = f"Application returned {response.status_code}. Fix the issue ! Restart the Application "
            send_notification(msg)

            # restart the application
            restart_container()

    except Exception as ex:
        print(f"Connection error happened: {ex}")
        # send email
        msg = f"Application not accessible at all. Fix the issue ! Restart the Application"
        send_notification(msg)
        restart_server_and_container()


schedule.every(5).minutes.do(monitor_application())
while True:
    schedule.run_pending()