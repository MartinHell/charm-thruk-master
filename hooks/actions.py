from charmhelpers.core import hookenv
import subprocess


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


