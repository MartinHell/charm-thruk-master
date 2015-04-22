#!/usr/bin/python

from charmhelpers.core import hookenv
from charmhelpers.core.services import helpers


class ThrukMasterRelation(helpers.RelationContext):
    """
    Relation context for the `thruk-agent` interface.
    """

    name = 'thruk-agent'
    interface = 'thruk-agent'
    #required_keys = ['host', 'port', 'nagios_context', 'thruk_key', 'thruk_id']

    def get_data(self):
        """ jinja won't allow hyphens in identifiers, so we switch to
        underscores here. """
        super(ThrukMasterRelation, self).get_data()
        if not hookenv.relation_ids(self.name):
            return
        self['host'] = hookenv.relation_get('host'),
        self['port'] = hookenv.relation_get('port'),
        self['nagios_context'] = hookenv.relation_get('nagios_context'),
        self['thruk_key'] = hookenv.relation_get('thruk_key'),
        self['thruk_id'] = hookenv.relation_get('thruk_id'),

        self['thruk_agent'] = self[self.name]
