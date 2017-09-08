from smtplib import SMTP
from nose.tools import assert_raises
from utils.email import smtp_init, email_body


good_credentials = {
    'server':'smtp.gmail.com',
    'port':'587',
    'username':'ltais.test',
    'password':'dfgh3456'
}

bad_credentials = {
    'server':'localhost',
    'port':'587',
    'username':'ltais.test',
    'password':'dfgh3456'
}


def test_smtp_init_ok():
    smtp_conn = smtp_init(good_credentials)
    assert smtp_conn.__class__ == SMTP


def test_smtp_init_error():
    assert_raises(Exception, smtp_init, bad_credentials)


# TEST BODY CONTENT
