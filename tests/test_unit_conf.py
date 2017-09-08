from nose.tools import assert_raises
from utils.conf import load_server_conf


def test_load_server_conf_ok():
    conf = load_server_conf('tests/good_conf.xml')
    assert 'database' in conf
    assert conf['database']['user'] == 'ltais'
    assert 'smtp' in conf
    assert conf['smtp']['port'] == '587'
    assert 'clients' in conf
    assert conf['clients'][0]['password'] == 'password'


def test_load_server_conf_missing_element():
    assert_raises(Exception, load_server_conf, 'tests/conf_missing_clients.xml')


def test_load_server_conf_missing_attribute():
    assert_raises(Exception, load_server_conf, 'tests/conf_missing_port.xml')


def test_load_server_conf_malformed():
    assert_raises(Exception, load_server_conf, 'tests/conf_malformed.xml')
