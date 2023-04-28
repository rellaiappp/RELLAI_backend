import smtplib
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_email_code(file):
    HTMLFile = open(file, "r")
    data = HTMLFile.read()
    return data

def sendConfirmationEmail(receiver, project_id):
    body = load_email_code('api/api_v1/endpoints/mail_template.html')
    sender = 'info@rellai.com'
    receivers = [receiver]
    msg = MIMEMultipart()

    msg['Subject'] = f'Project id confirmation: {project_id}'
    msg['From'] = 'info@rellai.com'
    msg['To'] = receiver
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP('smtp.hostinger.com', 587) as server:
            server.login('info@rellai.com', 'Rellai23!')
            server.sendmail(sender, receivers, msg.as_string())
            print("Successfully sent email")
        return True
    except Exception as e:
        print(e)
        return False

