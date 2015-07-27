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
import os
import urllib

import commons

from cloudify.decorators import operation


@operation
def deploy_grid(**kwargs):
    grid_name = kwargs['grid_name']
    schema = kwargs['schema']
    partitions = str(kwargs['partitions'])
    backups = str(kwargs['backups'])
    max_per_vm = str(kwargs['max_per_vm'])
    max_per_machine = str(kwargs['max_per_machine'])

    deployment_command = [
        commons.get_gs_script_path(),
        'deploy-space',
        '-cluster',
        'schema=%s total_members=%s,%s' % (schema, partitions, backups),
        '-max-instances-per-vm ' + max_per_vm,
        '-max-instances-per-machine ' + max_per_machine,
        grid_name
    ]

    commons.run_command(deployment_command)


@operation
def undeploy_grid(**kwargs):
    grid_name = kwargs['grid_name']

    deployment_command = [
        commons.get_gs_script_path(),
        'undeploy',
        grid_name
    ]

    commons.run_command(deployment_command)


@operation
def deploy_pu(**kwargs):
    pu_url = kwargs['pu_url']
    override_pu_name = kwargs['override_pu_name']
    schema = kwargs['schema']
    partitions = str(kwargs['partitions'])
    backups = str(kwargs['backups'])
    max_per_vm = str(kwargs['max_per_vm'])
    max_per_machine = str(kwargs['max_per_machine'])

    pu_name, pu_location = download_pu(pu_url, override_pu_name)

    deployment_command = [
        commons.get_gs_script_path(),
        'deploy',
        '-cluster',
        'schema=%s total_members=%s,%s' % (schema, partitions, backups),
        '-max-instances-per-vm ' + max_per_vm,
        '-max-instances-per-machine ' + max_per_machine,
        '-override-name ' + pu_name,
        pu_location
    ]

    commons.run_command(deployment_command)


def download_pu(pu_url, override_pu_name):
    ensure_pu_dir()

    jar_name = pu_url.split('/')[-1]
    pu_location = os.path.join(commons.TMPDIR, jar_name)
    urllib.urlretrieve(pu_url, pu_location)
    pu_name = override_pu_name if override_pu_name else jar_name.split('.jar')[0]

    return pu_name, pu_location


def ensure_pu_dir():
    pu_dir = os.path.join(commons.TMPDIR, 'pus')
    if not os.path.exists(pu_dir):
        os.makedirs(pu_dir)
