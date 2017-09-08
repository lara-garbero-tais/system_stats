from pymysql.cursors import Cursor
from nose.tools import assert_raises
from utils.db import db_init, db_insert_query


good_credentials = {
    'host': 'localhost',
    'user': 'ltais',
    'passwd':'asd101',
    'db':'ltais'
}

bad_credentials = {
    'host': 'localhost',
    'user': 'ltais',
    'passwd':'asd102',
    'db':'ltais'
}


def test_db_init_ok():
    db_cursor = db_init(good_credentials)
    assert type(db_cursor) == Cursor


def test_db_init_error():
    assert_raises(Exception, db_init, bad_credentials)
