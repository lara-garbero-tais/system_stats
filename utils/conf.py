import xml.etree.ElementTree as ET


DB_ATTR = ['host', 'username', 'password', 'db']
SMTP_ATTR = ['server', 'username', 'password', 'port']
CLIENT_ATTR = ['ip', 'port', 'username', 'password', 'mail']
ALERT_ATTR = ['type', 'limit']
ALERT_TYPES = ['memory', 'cpu', 'uptime']


def valid_alert(alert):
    return all(k in alert for k in ALERT_ATTR) and alert['type'] in ALERT_TYPES


def load_server_conf(file):

    """Parses a config XML file into a Python dict"""

    xml = ET.parse(file).getroot()
    conf = {'clients': []}

    # Load and validate database info
    db = xml.find('database')
    try:
        database = db.attrib
    except AttributeError:
        raise Exception('<database> element not present in {}'.format(file))
    if not all(key in database for key in DB_ATTR):
        raise Exception('malformed <database> element.')
    else:
        # These are renamed at this point to keep config.xml consistent
        renamed_database_attrs = {}
        renamed_database_attrs['host'] = database['host']
        renamed_database_attrs['user'] = database['username']
        renamed_database_attrs['passwd'] = database['password']
        renamed_database_attrs['db'] = database['db']
        conf['database'] = renamed_database_attrs


    # Load and validate SMTP server info
    db = xml.find('smtp')
    try:
        conf['smtp'] = db.attrib
    except AttributeError:
        raise Exception('<smtp> element not present in {}'.format(file))
    if not all(key in conf['smtp'] for key in SMTP_ATTR):
        raise Exception('malformed <smtp> element.')


    # Load and validate clients info
    try:
        clients = xml.find('clients').findall('client')
    except AttributeError:
        raise Exception('<clients> element not present in {}'.format(file))

    for client in clients:
        client_info = client.attrib
        alerts = []
        alert_nodes = client.findall('alert')
        for alert_node in alert_nodes:
            if valid_alert(alert_node.attrib):
                alerts.append((alert_node.attrib['type'],
                              alert_node.attrib['limit'].rstrip('%')))
        client_info['alerts'] = alerts
        if all(key in client_info for key in CLIENT_ATTR):
            conf['clients'].append(client_info)
    if conf['clients'] == []:
        raise Exception('No correctly formed <client> elements found')

    return conf
