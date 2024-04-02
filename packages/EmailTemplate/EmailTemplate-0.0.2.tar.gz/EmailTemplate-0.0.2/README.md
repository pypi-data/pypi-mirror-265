# EmailTemplate
    This is to allow beginners to easily send emails.

## emailtablenofile
    This is used to send a HTML file created by pandas in the email by passing
    the html table direclty to the template.

    Requirements:
        host= SMTP address
        sender = Senders email address
        password = Senders password
        port = Senders email port address
        reciver = Who is getting the email
        title = subject line to the email.
        text = the bodys text
        html = the HTML content for the email.

## emailtextnofile
    This is used to send emails with text only.

    Requirments:
        host= SMTP address
        sender = Senders email address
        password = Senders password
        port = Senders email port address
        reciver = Who is getting the email
        title = subject line to the email.
        text = the bodys text

## emailwithfile
    This is used to send emails with a file attached.

    Requirments:
        host= SMTP address
        sender = Senders email address
        password = Senders password
        port = Senders email port address
        reciver = Who is getting the email
        title = subject line to the email.
        text = the bodys text
        filepath = the file you want to send.