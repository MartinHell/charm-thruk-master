from charmhelpers.core import hookenv
import subprocess
import os
import base64


def log_start(service_name):
    hookenv.log('thruk-master starting')


def pwgen():
    return str(subprocess.check_output(['pwgen', '-s', '16'])).strip()


def thruk_set_password(service_name):
    passwd_file = "/var/lib/thruk/thrukadmin.passwd"
    if not os.path.exists(passwd_file):
        password = pwgen()
        with open(passwd_file, 'w') as pfile:
            pfile.write(password)
            os.chmod(pfile.name, 0600)

        ret = subprocess.call(["/usr/bin/htpasswd", "-b", "/etc/thruk/htpasswd",
                              "thrukadmin", password])
        if not ret:
            hookenv.log('WARNING: thruk htpassword reset failed!')
    else:
        with open(passwd_file) as pfile:
            password = pfile.read().strip()


def thruk_fix_ssl(service_name):

    if hookenv.config['trusted_ssl_cert']:
        cert_file = None
        if hookenv.config['trusted_ssl_certlocation']:
            cert_file = '/usr/local/share/ca-certificates/%s' % \
                (hookenv.config['trusted_ssl_certlocation'].rpartition('/')[2])

        trusted_ssl_cert = hookenv.config['trusted_ssl_cert']
        hookenv.log("Writing cert from trusted_ssl_cert: %s" % trusted_ssl_cert)
        with open(cert_file, 'w') as f:
            f.write(str(base64.b64decode(trusted_ssl_cert)))

        subprocess.call(["/usr/sbin/update-ca-certificates"])
