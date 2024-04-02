#!/usr/bin/env python3

##################################################
## Email Module
##################################################
## Author: David Billingsley
## Copyright: Copyright 2023
## License: Unlicensed
## Version: 0.0.1
## Maintainer: David Billingsley
## Email: daveandtaybillingsley@gmail.com
## Status: Production
##################################################
## Uses: Sends emails based on the functions below
##################################################

import ssl
from email.message import EmailMessage
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def emailtablenofile(host, sender, password, port, receiver, title, text, html):
    msg = MIMEMultipart('alternative', None)

    msg['Subject'] = title
    msg['From'] = sender
    msg['To'] = receiver

    p1 = MIMEText(text, 'plain')
    p2 = MIMEText(html, 'html')

    msg.attach(p1)
    msg.attach(p2)

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        print('Email Sent')


def emailtextnofile(host, sender, password, port, receiver, title, text):
    msg = EmailMessage()

    msg['Subject'] = {title}
    msg['From'] = sender
    msg['To'] = receiver

    message = f"""\
                    {text}
                    """

    msg.set_content(message)

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        print('Email Sent')


def emailwithfile(host, sender, password, port, receiver, title, text, filepath):
    subject = title
    body = f"{text}"
    sender_email = sender
    receiver_email = receiver
    passwordval = password

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Open PDF file in binary mode
    with open(filepath, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filepath}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP(host, port) as server:
        server.starttls(context=context)
        server.login(sender_email, passwordval)
        server.sendmail(sender_email, receiver_email, text)
