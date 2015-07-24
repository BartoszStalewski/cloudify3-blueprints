########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and

# * limitations under the License.
import json

import commons

from cloudify import ctx
from cloudify.decorators import operation


def list_to_str(lst):
    return str(json.dumps(lst))


@operation
def deploy_gateway_space(**kwargs):
    script = "xap-scripts/deploy-space-with-gateway.groovy"
    spacename = kwargs['space_name']
    spacezones = kwargs['space_zones']
    gwname = kwargs['gateway_name']
    targets = kwargs['gateway_targets']
    script_path = ctx.download_resource(script)
    ctx.download_resource("xap-scripts/space-pu.xml", "/tmp/space-pu.xml")

    locators = commons.read_locators()
    ip = commons.get_ip_from_interface_name(ctx.node.properties['interfacename'])
    space_deployment_command = [
        commons.get_groovy_path(),
        "-Dspacename=" + spacename,
        "-Dzones=" + spacezones,
        "-Dtargets=" + list_to_str(targets),
        "-Dgwname=" + gwname,
        "-Dlocallocators=" + locators,
        "-Djava.rmi.server.hostname=" + ip,
        script_path
    ]

    commons.run_command(space_deployment_command)


@operation
def deploy_gateway_pu(**kwargs):
    script = "xap-scripts/deploy-gateway.groovy"
    puname = kwargs['space_name'] + "-gw"
    spacename = kwargs['space_name']
    gwname = kwargs['gateway_name']
    gatewayzones = kwargs['gateway_zones']
    targets = kwargs['gateway_targets']
    sources = kwargs['gateway_sources']
    lookups = kwargs['gateway_lookups']
    natmappings = kwargs['gateway_natmappings']
    script_path = ctx.download_resource(script)
    ctx.download_resource("xap-scripts/gateway-pu.xml", "/tmp/gateway-pu.xml")
    locators = commons.read_locators()

    ip = commons.get_ip_from_interface_name(ctx.node.properties['interfacename'])
    mylocators = {'gwname': gwname, 'address': ip, 'discoport': kwargs['gateway_discoport'],
                  'commport': kwargs['gateway_commport']}
    lookups.append(mylocators)

    gateway_deployment_command = [
        commons.get_groovy_path(),
        "-Dpuname=" + puname,
        "-Dspacename=" + spacename,
        "-Dzones=" + gatewayzones,
        "-Dtargets=" + list_to_str(targets),
        "-Dgwname=" + gwname,
        "-Dlocallocators=" + locators,
        "-Dlocalgwname=" + gwname,
        "-Dsources=" + list_to_str(sources),
        "-Dlookups=" + list_to_str(lookups),
        "-Dnatmappings=" + natmappings,
        "-Djava.rmi.server.hostname=" + ip,
        script_path
    ]

    commons.run_command(gateway_deployment_command, ip, locators)


@operation
def deploy_rest(**kwargs):
    spacename = kwargs['space_name']
    port = kwargs['rest_port']
    zones = kwargs['rest_zones']

    rest_deployment_command = [
        commons.get_gs_script_path(),
        "deploy-rest",
        "-spacename " + spacename,
        "-port " + str(port)
    ]
    if len(zones) > 0:
        rest_deployment_command.append("-zones " + zones)

    commons.run_command(rest_deployment_command)
