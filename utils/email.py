import smtplib


def smtp_init(credentials):

    """Initializes a connection to the SMTP server"""

    try:
        mailserver = smtplib.SMTP(credentials['server'], credentials['port'])
    except Exception as e:
        raise Exception('SMTP server error: Wrong hostname or port.')
    mailserver.starttls()
    mailserver.ehlo()
    try:
        mailserver.login(credentials['username'], credentials['password'])
    except Exception as e:
        raise Exception('Error connecting to SMTP server.')
    return mailserver


def email_body(client, data):

    body = '\r\n'
    warning_list = ''

    for alert in client['alerts']:
        try:
            limit = float(alert[1])
        except Exception as E:
            # Non-numeric values are ignored
            continue

        if alert[0] == 'memory' and limit < data[0]:
            warning_list += "Memory usage has exceeded {}%. ".format(limit)
        if alert[0] == 'cpu' and limit < data[1]:
            warning_list += "CPU usage has exceeded {}%. ".format(alimit)
        if alert[0] == 'uptime' and limit < data[2]:
            warning_list += "Uptime has exceeded {} seconds. ".format(limit)

    if warning_list is not '':
        body += 'WARNING: '
        body += warning_list
        body += '\r\n'

    body += 'Memory: {0}%. CPU: {1}%. Uptime: {2} seconds.'.format(*data)

    return body
