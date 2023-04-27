import smtplib
import traceback
from email.mime.text import MIMEText

def sendConfirmationEmail(receiver, project_id):
    sender = 'info@rellai.com'
    receivers = [receiver]
    msg = MIMEText('This is test mail')

    msg['Subject'] = f'Project id confirmation: {project_id}'
    msg['From'] = 'info@rellai.com'
    msg['To'] = receiver

    try:
        with smtplib.SMTP('smtp.hostinger.com', 587) as server:
            server.login('info@rellai.com', 'Rellai23!')
            server.sendmail(sender, receivers, msg.as_string())
            print("Successfully sent email")
        return True
    except Exception as e:
        print(e)
        return False
