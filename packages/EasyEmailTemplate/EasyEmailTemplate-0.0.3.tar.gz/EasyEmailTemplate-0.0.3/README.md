# EmailTemplate
    This is to allow beginners to easily send emails.  This project contains some
    basic templates.

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

    Example:
    The following code block creates a html template to be added with the pandas
    dataframe to create a table and output to html to pass the the template for
    the email to send out.

```
    message_style = """
<html>
  <head><title>HTML Pandas Dataframe with CSS</title></head>
  <link rel="stylesheet" type="text/css" href="df_style.css"/>

  <style type="text/css" media="screen">
      #mystyle {
    font-size: 11pt;
    font-family: Arial;
    border-collapse: collapse;
    border: 1px solid silver;

  }

  #mystyle td,
  th {
    padding: 5px;
    text-align: center;
    vertical-align: center;
  }

  #mystyle tr:nth-child(even) {
    background: #E0E0E0;
    text-align: center;
    vertical-align: center;
  }

  #mystyle tr:hover {
    background: silver;
    cursor: pointer;
    text-align: center;
    vertical-align: center;
    font-weight: bold;
  }
  </style>
</head>
  <body>
"""
result = df.to_html(index=False, render_links=True, table_id="mystyle", escape=False)
```

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