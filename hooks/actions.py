from charmhelpers.core import hookenv


def log_start(service_name):
    hookenv.log('thruk-master starting')
