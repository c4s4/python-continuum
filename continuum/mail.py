#!/usr/bin/env python
# encoding: UTF-8

import os
import sys
import getopt
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart


ENCODING = 'UTF-8'
SMTP_HOST = 'smtp.orange.fr'
RECIPIENT = 'michel.casabianca@gmail.com'
SENDER = RECIPIENT


def _binary(string):
    if isinstance(string, str):
        return string.encode(ENCODING)
    elif isinstance(string, list):
        return [_binary(e) for e in string]
    else:
        return str(string)


def send(subject, text, sender=SENDER, recipients=[RECIPIENT], attachments={}, smtp_host=SMTP_HOST, encoding=ENCODING):
    # encode all strings in binary strings
    subject = _binary(subject)
    text = _binary(text)
    sender = _binary(sender)
    if not isinstance(recipients, list):
        recipients = [recipients]
    recipients = _binary(recipients)
    # build the message
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = ', '.join(recipients)
    # attach text part
    message.attach(MIMEText(text, _charset=encoding))
    # attach attachments if any
    for name,filename in list(attachments.items()):
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(filename,"rb").read())
        encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % name)
        message.attach(part)
    smtp = smtplib.SMTP(smtp_host)
    smtp.sendmail(sender, recipients, message.as_string())
    smtp.quit()


HELP = '''mail.py [-h] -f from -r recipient -s subject -a file -m smtphost -e encoding message
Send an email with following:
-h            Print this help page
-f from       The mail sender
-r recipient  The mail recipient(s)
-s subject    The mail subject
-a file       A file to attach
-m smtphost   The SMTP server host
-e encoding   The encoding to use
message       The message'''


if __name__ == '__main__':
    _sender     = SENDER
    _recipients = []
    _subject    = None
    _attach     = {}
    _smtp       = SMTP_HOST
    _encoding   = ENCODING
    _message    = None
    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:], "hf:r:s:a:m:e:", ["help", "from", "recipient", "subject", "attachement", "smtp", "encoding"])
    except getopt.GetoptError as error:
        print("ERROR: %s" % str(error))
        print(HELP)
        sys.exit(1)
    for OPT, ARG in OPTS:
        if OPT == '-h' or OPT == '--help':
            print(HELP)
            sys.exit(0)
        elif OPT == '-f' or OPT == '--from':
            _sender = ARG
        elif OPT == '-r' or OPT == '--recipient':
            _recipients.append(ARG)
        elif OPT == '-s' or OPT == '--subject':
            _subject = ARG
        elif OPT == '-a' or OPT == '--attach':
            _name = os.path.basename(ARG)
            _attach[_name] = ARG
        elif OPT == '-m' or OPT == '--smtp':
            _smtp = ARG
        elif OPT == '-e' or OPT == '--encoding':
            _encoding = ARG
        else:
            print("Unhandled option: %s" % OPT)
            print(HELP)
            sys.exit(1)
    _message = ' '.join(ARGS)
    if len(_recipients) < 1:
        _recipients = [RECIPIENT]
    if not _subject:
        print("Missing subject")
        print(HELP)
        sys.exit(1)
    if not _message:
        print("Missing message")
        print(HELP)
        sys.exit(1)
    send(_subject, _message, _sender, _recipients, _attach, _smtp, _encoding)
