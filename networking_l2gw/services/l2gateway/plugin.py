# Copyright (c) 2015 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from neutron.common import exceptions as n_exc
from neutron.db import servicetype_db as st_db
from neutron import manager
from neutron.services import provider_configuration as pconf
from neutron.services import service_base

from networking_l2gw._i18n import _LE
from networking_l2gw.db.l2gateway import l2gateway_db
from networking_l2gw.services.l2gateway.common import config
from networking_l2gw.services.l2gateway.common import constants

from oslo_log import log as logging

LOG = logging.getLogger(__name__)


def add_provider_configuration(type_manager, service_type):
    type_manager.add_provider_configuration(
        service_type,
        pconf.ProviderConfiguration('networking_l2gw'))


class L2GatewayPlugin(l2gateway_db.L2GatewayMixin):

    """Implementation of the Neutron l2 gateway Service Plugin.

    This class manages the workflow of L2 gateway request/response.
    """

    supported_extension_aliases = ["l2-gateway",
                                   "l2-gateway-connection"]

    def __init__(self):
        """Do the initialization for the l2 gateway service plugin here."""
        config.register_l2gw_opts_helper()
        self.service_type_manager = st_db.ServiceTypeManager.get_instance()
        add_provider_configuration(self.service_type_manager, constants.L2GW)
        self._load_drivers()
        super(L2GatewayPlugin, self).__init__()
        l2gateway_db.subscribe()

    def _load_drivers(self):
        """Loads plugin-drivers specified in configuration."""
        self.drivers, self.default_provider = service_base.load_drivers(
            'L2GW', self)

    def _get_driver_for_provider(self, provider):
        if provider in self.drivers:
            return self.drivers[provider]
        # raise if not associated (should never be reached)
        raise n_exc.Invalid(_LE("Error retrieving driver for provider %s") %
                            provider)

    @property
    def _core_plugin(self):
        return manager.NeutronManager.get_plugin()

    def get_plugin_type(self):
        """Get type of the plugin."""
        return constants.L2GW

    def get_plugin_description(self):
        """Get description of the plugin."""
        return constants.L2_GATEWAY_SERVICE_PLUGIN

    def add_port_mac(self, context, port_dict):
        """Process the created port and trigger the RPC

        to add to the gateway.
        """
        self._get_driver_for_provider(constants.l2gw
                                      ).add_port_mac(context, port_dict)

    def delete_port_mac(self, context, port):
        """Process the deleted port and trigger the RPC

        to delete from the gateway.

        When the ML2 plugin invokes this call, the argument port is
        a single port dict, whereas the L2gateway service plugin
        sends it as a list of port dicts.
        """
        self._get_driver_for_provider(constants.l2gw
                                      ).delete_port_mac(context, port)

    def create_l2_gateway_connection(self, context, l2_gateway_connection):
        """Process the call from the CLI and trigger the RPC,

        to update the connection to the gateway.
        """
        self._get_driver_for_provider(constants.l2gw
                                      ).create_l2_gateway_connection(
            context, l2_gateway_connection)
        return super(L2GatewayPlugin, self).create_l2_gateway_connection(
            context, l2_gateway_connection)

    def delete_l2_gateway_connection(self, context, l2_gateway_connection):
        """Process the call from the CLI and trigger the RPC,

        to update the connection from the gateway.
        """
        self._get_driver_for_provider(constants.l2gw
                                      ).delete_l2_gateway_connection(
            context, l2_gateway_connection)
        return super(L2GatewayPlugin, self).delete_l2_gateway_connection(
            context, l2_gateway_connection)
