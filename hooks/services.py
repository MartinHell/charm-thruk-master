#!/usr/bin/python

from charmhelpers.core.services.base import ServiceManager
from charmhelpers.core.services import helpers
from charmhelpers.core import hookenv

import actions
import thruk_helpers


def manage():
    config = hookenv.config()
    manager = ServiceManager([
        {
            'service': 'thruk-master',
            'ports': [80, 443],  # ports to after start
            # 'provided_data': [
            #    # context managers for provided relations
            #    # e.g.: helpers.HttpRelation()
            # ],
            'required_data': [
                # data (contexts) required to start the service
                # e.g.: helpers.RequiredConfig('domain', 'auth_key'),
                #       helpers.MysqlRelation(),
                thruk_helpers.ThrukMasterRelation(),
                helpers.RequiredConfig(),
            ],
            'data_ready': [
                helpers.render_template(
                    source='thruk_local.conf',
                    target='/etc/thruk/thruk_local.conf'),
                helpers.render_template(
                    source='log4perl.conf',
                    target='/etc/thruk/log4perl.conf'),
                actions.log_start,
                actions.update_ppa,
                actions.thruk_set_password,
                actions.thruk_fix_ssl,
            ],
        },
        {
            'service': 'thruk-monitoring',
            'required_data': [
                thruk_helpers.NEMRelation(),
                helpers.RequiredConfig(),
            ],
            'data_ready': [
                helpers.render_template(
                    source='thruk-nrpe.j2',
                    target='/etc/nagios/nrpe.d/check_{}.cfg'.format(
                           hookenv.local_unit().replace('/', '-'),
                    )
                ),
                helpers.render_template(
                    source='thruk-nagios.j2',
                    target='/var/lib/nagios/export/service__{}-{}.cfg'.format(
                        config['nagios_context'],
                        hookenv.local_unit().replace('/', '-'),
                    )
                ),
            ],
         },
    ])
    manager.manage()
