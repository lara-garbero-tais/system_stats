import paramiko
from ast import literal_eval

from utils.conf import load_server_conf
from utils.db import db_init, db_insert_query
from utils.email import smtp_init, email_body


# Load config xml file
config = load_server_conf('config.xml')

# Initialize database connection
database = db_init(config['database'])

# Initialize SMTP server
smtp_server = smtp_init(config['smtp'])

# Initialize SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Process individual clients
for client in config['clients']:

    try:
        ssh.connect(client['ip'], 
                    username=client['username'], password=client['password'])
    except Exception as E:
        print('Cannot connect to client {}: Skipping.'.format(client['ip']))
        print(E.message)
        continue

    print('Processing {}:'.format(client['ip']))

    # Transfer client.py to remote
    mk_stdin, mk_stdout, mk_stderr = ssh.exec_command('mkdir /tmp/stats/')
    sftp = ssh.open_sftp()
    sftp.put('client.py', '/tmp/stats/client.py')
    sftp.close()


    load_profile = """
        . ~/.profile;
        . ~/.bash_profile;

    """

    # Find python3 
    py_in, py_out, py_err = ssh.exec_command(load_profile + 'which python3')
    py_path = py_out.read().rstrip().decode('utf-8')

    if py_path == '':
        print('No usable python3 found. Skipping.')
        continue

    # Excecute client script and read its output
    sh_in, sh_out, sh_err = ssh.exec_command(py_path + ' /tmp/stats/client.py')
    client_stats = literal_eval(sh_out.read().rstrip().decode('utf-8'))
    ssh.close()

    print(client_stats)

    database.execute(db_insert_query(client, client_stats))
    body = email_body(client, client_stats)
    smtp_server.sendmail(config['smtp']['server'], client['mail'], body)

smtp_server.quit()
