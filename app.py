# -*- coding: utf-8 -*-
import time
import re
import random
import os
import smtplib
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate


def send_mail(login, pwd, recipients, body, subject, from_):
    SMTP_SERVER = 'smtp.yandex.ru'
    SMTP_PORT = 587

    assert type(recipients) == list

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['To'] = ','.join(recipients)
    msg['From'] = '{0} <{1}>'.format(from_, login)
    msg['Date'] = formatdate(localtime=True)
    msg['Return-Path'] = login

    part = MIMEText('text', 'plain')
    part.set_payload(body)
    msg.attach(part)

    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

    session.ehlo()
    session.starttls()
    session.login(login, pwd)

    try:
        session.sendmail(login, recipients, msg.as_string())
        return True
    except:
        return False
    finally:
        session.quit()


def get_excerpt(source):
    chunksize = 2 * 1024
    EXCERPT_RE = r'[IVXL]+([\s\S]+?)[IVXL]+'

    with open(source, 'r') as f:
        filesize = os.stat(source).st_size
        pos = random.randint(0, int(filesize) - chunksize)
        f.seek(pos)
        f.readline()
        text = f.read(chunksize)
        while text[-1] != ' ':
            text += f.read(1)
        match = re.search(EXCERPT_RE, text)
        if match:
            text = match.group(1)
            return text[2:-2]
        else:
            return None


LOGIN, PWD = 'alex06.06.1799@yandex.ru', 'rskjgnrtkn34yu'
source = 'appdata.txt'
subject, body = 'An excerpt from my poem', get_excerpt(source)
recipient = '{0}@yandex.ru'.format(''.join([random.choice(string.ascii_lowercase) for i in xrange(6)]))
# recipient = 'your_email@yandex.ru'

time.sleep(random.randint(0, 5))

if body:
    print 'Sending email to {0}...'.format(recipient)
    if send_mail(LOGIN, PWD, [recipient], body, subject, 'Alex Pushkin'):
        print 'Success!'
        exit(0)
    else:
        print 'Failure'
        exit(1)
else:
    raise RuntimeError('Failed to send email')
