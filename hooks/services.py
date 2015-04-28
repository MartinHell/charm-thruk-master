#!/usr/bin/python

from charmhelpers.core.services.base import ServiceManager
from charmhelpers.core.services import helpers
# from charmhelpers.core import hookenv

import actions
import thruk_helpers


def manage():
    manager = ServiceManager([
        {
            'service': 'thruk-master',
            'ports': [80],  # ports to after start
            # 'provided_data': [
            #    # context managers for provided relations
            #    # e.g.: helpers.HttpRelation()
            # ],
            'required_data': [
                # data (contexts) required to start the service
                # e.g.: helpers.RequiredConfig('domain', 'auth_key'),
                #       helpers.MysqlRelation(),
                thruk_helpers.ThrukMasterRelation(),
            ],
            'data_ready': [
                helpers.render_template(
                    source='thruk_local.conf',
                    target='/etc/thruk/thruk_local.conf'),
                actions.log_start,
                actions.thruk_set_password,
                actions.thruk_fix_ssl,
            ],
        },
    ])
    manager.manage()
