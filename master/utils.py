import os
import smtplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

html_template_head_padding = '''
<html>
    <head></head>
    <body>
'''
html_template_foot_padding = '''
    </body>
</html>
'''


def send_email(message, frames):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header(message, 'utf-8')
    msg['From'] = "n1"
    htm = ''
    for i, frame in enumerate(frames):
        image_msg = MIMEImage(frame)
        image_msg.add_header('Content-ID', f'<image{i}>')
        msg.attach(image_msg)
        htm += f'''<br><img src="cid:image{i}"/></br>'''
    msg.attach(MIMEText(html_template_head_padding + htm + html_template_foot_padding, 'html'))
    server = smtplib.SMTP(os.getenv('WDS_SMTP_SERVER'), int(os.getenv('WDS_SMTP_PORT')))
    server.set_debuglevel(0)
    server.starttls()
    server.login(os.getenv('WDS_SENDER_EMAIL'), os.getenv('WDS_SENDER_PASSWORD'))
    server.sendmail(os.getenv('WDS_SENDER_EMAIL'), eval(os.getenv('WDS_RECEIVER_EMAILS')), msg.as_string())
    server.quit()

