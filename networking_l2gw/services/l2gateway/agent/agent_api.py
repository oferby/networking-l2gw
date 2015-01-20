# Copyright (c) 2015 OpenStack Foundation.
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

from neutron.common import rpc as n_rpc

from oslo import messaging


class L2GatewayAgentApi(object):
    """Agent side of the Agent to Plugin RPC API."""

    API_VERSION = '1.0'

    def __init__(self, topic, context, host):
        self.context = context
        self.host = host
        target = messaging.Target(topic=topic, version=self.API_VERSION)
        self.client = n_rpc.get_client(target)

    def update_ovsdb_changes(self, ovsdb_data):
        cctxt = self.client.prepare()
        return cctxt.call(self.context,
                          'update_ovsdb_changes',
                          ovsdb_data=ovsdb_data)
