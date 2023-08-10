import logging.config
import os
import socket

from configparser import ConfigParser

from lib.utils.log_utils import get_logger

__import__('cloghandler')

version = '0.1.0'
current_path = os.path.dirname(__file__)
project_path = os.path.dirname(current_path)
config_path = os.path.join(project_path, 'etc/app.cfg')
true_false_map = (lambda x: True if x == '1' else False)
cf = ConfigParser()
cf.read(config_path)


################################################################
# mysql database
################################################################
def get_mysql_db_info():
    host = cf.get('mysql', 'host')
    port = int(cf.get('mysql', 'port'))
    user = cf.get('mysql', 'user')
    password = cf.get('mysql', 'password')
    db = cf.get('mysql', 'db')
    return host, port, db, user, password


################################################################
# logger
################################################################
log_file = os.path.join(project_path, 'logs/app.log')
error_log_file = os.path.join(project_path, 'logs/app_error.log')
debug_log_file = os.path.join(project_path, 'logs/app_debug.log')
logging.config.fileConfig(
    os.path.join(project_path, 'etc/log.cfg'),
    defaults={
    'log_filename': log_file,
    'debug_log_filename': debug_log_file,
    'error_log_filename': error_log_file,
    }
)


################################################################
# main
################################################################
debug = true_false_map(cf.get('main', 'debug'))
