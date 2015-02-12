# Copyright 2015 OpenStack Foundation
# Copyright (c) 2015 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from neutron.api.v2 import base
from neutron.common import exceptions

from webob import exc as web_exc


class L2GatewayInUse(exceptions.InUse):
    message = _("L2 Gateway '%(gateway_id)s' still has active mappings "
                "with one or more neutron networks.")


class L2GatewayNotFound(exceptions.NotFound):
    message = _("L2 Gateway %(gateway_id)s could not be found")


class L2GatewayDeviceInUse(exceptions.InUse):
    message = _("L2 Gateway Device '%(device_id)s' is still used by "
                "one or more network gateways.")


class L2GatewayDeviceNotFound(exceptions.NotFound):
    message = _("L2 Gateway Device %(device_id)s could not be found.")


class L2GatewayPortInUse(exceptions.InUse):
    message = _("Port '%(port_id)s' is owned by '%(device_owner)s' and "
                "therefore cannot be deleted directly via the port API.")


class L2GatewayConnectionExists(exceptions.InUse):
    message = _("The specified mapping '%(mapping)s' exists on "
                "network gateway '%(gateway_id)s'.")


class L2MultipleGatewayConnections(exceptions.NeutronException):
    message = _("Multiple network connections found on '%(gateway_id)s' "
                "with provided criteria.")


class L2GatewayInterfaceNotFound(exceptions.NeutronException):
    message = _("L2 Gateway interface not found on '%(interface_id)s'")


class L2GatewayConnectionNotFound(exceptions.NotFound):
    message = _("The connection %(id)s was not found on the l2 gateway")


base.FAULT_MAP.update({L2GatewayInUse: web_exc.HTTPConflict,
                       L2GatewayPortInUse: web_exc.HTTPConflict,
                       L2GatewayConnectionExists: web_exc.HTTPConflict,
                       L2GatewayConnectionNotFound: web_exc.HTTPNotFound,
                       L2MultipleGatewayConnections: web_exc.HTTPConflict})