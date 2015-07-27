########
# Copyright (c) 2015 GigaSpaces Technologies Ltd. All rights reserved
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
import commands
import os
import subprocess

from cloudify import ctx


TMPDIR = os.path.join(os.sep, 'tmp')


def get_ip_from_interface_name(interface_name):
    intf_ip = commands.getoutput('ip address show dev ' + interface_name).split()
    intf_ip = intf_ip[intf_ip.index('inet') + 1].split('/')[0]
    return intf_ip


def run_command(command, ip=None, locators=None):
    my_env = os.environ.copy()
    my_env['LOOKUPLOCATORS'] = locators or read_locators()
    my_env['NIC_ADDR'] = ip or get_ip_from_interface_name(ctx.node.properties['interfacename'])

    ctx.logger.info("Executing: %s", command)
    output = subprocess.check_output(command, env=my_env)
    ctx.logger.info("Finished executing, output: %s", output)


def read_locators():
    locators = os.path.join(TMPDIR, 'locators')
    return ','.join([line.strip() for line in open(locators)])


def get_gs_script_path():
    return os.path.join(get_xap_dir(), 'bin', 'gs.sh')


def get_groovy_path():
    return os.path.join(get_xap_dir(), 'tools', 'groovy', 'bin', 'groovy')


def get_xap_dir():
    gsdir = os.path.join(TMPDIR, 'gsdir')
    return ''.join([line.strip() for line in open(gsdir)])
