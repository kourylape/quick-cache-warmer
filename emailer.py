import smtplib
import os
import sys
from dotenv import Dotenv
from email import Encoders
from email.MIMEBase import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailerError(Exception):
    def __init__(self, message):
        super(EmailerError, self).__init__(message)


class Emailer:

    def __init__(self):
        # get settings from .env file
        settings = dict(
            name='Quick Cache Warmer',
            server=os.environ.get('SMTP_SERVER', ''),
            username=os.environ.get('SMTP_USERNAME', ''),
            password=os.environ.get('SMTP_PASSWORD', ''),
            port=os.environ.get('SMTP_PORT', ''),
            reply=os.environ.get('SMTP_FROM', ''),
            recipients=os.environ.get('SMTP_RECIPIENTS', '')
        )
        # check settings
        all_req = ['server', 'username', 'password', 'port',
                   'name', 'reply', 'recipients']
        if not all(k in settings for k in all_req):
            msg = '----- EMAIL SETTINGS ERROR -----\n'
            msg += 'You are missing 1 more of the required fields!\n'
            msg += 'The following fields are required: '
            msg += '[%s]' % ', '.join(all_req)
            raise EmailerError(msg)
        else:
            self.settings = settings

        # connect to mail server
        self.__connect()

    def __connect(self):
        s = self.settings
        try:
            smtpserver = smtplib.SMTP(s['server'], s['port'])
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            smtpserver.login(s['username'], s['password'])
            self.smtp = smtpserver
        except:
            raise EmailerError('ERROR - Could not connect to the SMTP server. '
                               'Check your settings and try again.')

    def send_email(self, message, subject, attachments=[]):
        s = self.settings

        try:
            msg = MIMEMultipart('alternative')
            msg['To'] = s['recipients']
            msg['From'] = '%s<%s>' % (s['name'], s['reply'])
            msg['Subject'] = subject

            # add any attachments
            if len(attachments) > 0:
                for f in attachments:
                    part = MIMEBase('application', "octet-stream")
                    part.set_payload(open(f, "rb").read())
                    Encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        'attachment; filename="%s"' % os.path.basename(f))
                    msg.attach(part)

            msg.attach(MIMEText(message, 'html'))

            self.smtp.sendmail(s['reply'], s['recipients'], msg.as_string())
        except Exception as e:
            print e
            raise EmailerError('ERROR - Could not successfully send email!')

    def __del__(self):
        if hasattr(self, 'smtp'):
            self.smtp.close()
