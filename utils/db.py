import pymysql


def db_init(credentials):

    """Initializes a DB connection"""
    
    try:
        db = pymysql.connect(**credentials)
    except pymysql.err.OperationalError:
        raise Exception('Error connecting to database.')
    return db.cursor()


def db_insert_query(client, data):

    """Formats SQL"""

    query = """INSERT INTO client_stats (ip, memory, cpu, uptime) 
               VALUES ("{0}", {1}, {2}, {3});""".format(client['ip'],
                                                        data[0],
                                                        data[1],
                                                        data[2]
                                                )
    return query
