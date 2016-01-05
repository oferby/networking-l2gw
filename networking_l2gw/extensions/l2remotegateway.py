import abc

from neutron.api import extensions
from neutron.api.v2 import attributes
from neutron.api.v2 import resource_helper

from networking_l2gw.services.l2gateway.common import constants

RESOURCE_ATTRIBUTE_MAP = {
    constants.L2_REMOTE_GATEWAYS: {
        'id': {'allow_post': False, 'allow_put': False,
               'is_visible': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': None},
                 'is_visible': True, 'default': ''},
        'ipaddr': {'allow_post': True, 'allow_put': True,
                    'validate': {'type:string': None},
                    'is_visible': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'validate': {'type:string': None},
                      'required_by_policy': True,
                      'is_visible': True}
    },
}


class L2remotegateway(extensions.ExtensionDescriptor):

    """API extension for Remote Gateway """

    @classmethod
    def get_name(cls):
        return "L2 Remote Gateway"

    @classmethod
    def get_alias(cls):
        return "l2-remote-gateway"

    @classmethod
    def get_description(cls):
        return "Define a remote gateway that can be used to connect to remote Neutron networks"

    @classmethod
    def get_updated(cls):
        return "2015-12-31T00:00:00-00:00"

    @classmethod
    def get_resources(cls):
        """Returns Ext Resources."""
        mem_actions = {}
        plural_mappings = resource_helper.build_plural_mappings(
            {}, RESOURCE_ATTRIBUTE_MAP)
        attributes.PLURALS.update(plural_mappings)
        resources = resource_helper.build_resource_info(plural_mappings,
                                                        RESOURCE_ATTRIBUTE_MAP,
                                                        constants.L2GW,
                                                        action_map=mem_actions,
                                                        register_quota=True,
                                                        translate_name=True)
        return resources

    def get_extended_resources(self, version):
        if version == "2.0":
            return RESOURCE_ATTRIBUTE_MAP
        else:
            return {}


class L2RemoteGatewayPluginBase(extensions.PluginInterface):

    @abc.abstractmethod
    def get_l2_remote_gateways(self, context, filters=None,
                               fields=None,
                               sorts=None, limit=None, marker=None,
                               page_reverse=False):
        pass

    @abc.abstractmethod
    def create_l2_remote_gateway(self, context, l2_remote_gateway):
        pass

    @abc.abstractmethod
    def get_l2_remote_gateway(self, context, id, fields=None):
        pass

    @abc.abstractmethod
    def delete_l2_remote_gateway(self, context, id):
        pass

    @abc.abstractmethod
    def update_l2_remote_gateway(self, context, id, l2_remote_gateway):
        pass

