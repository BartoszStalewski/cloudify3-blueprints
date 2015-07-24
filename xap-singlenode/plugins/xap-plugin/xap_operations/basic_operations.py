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

from cloudify import ctx
from cloudify.decorators import operation


@operation
def deploy_grid(**kwargs):
    grid_name = kwargs["grid_name"]
    schema = kwargs["schema"]
    partitions = str(kwargs["partitions"])
    backups = str(kwargs["backups"])
    max_per_vm = str(kwargs["max_per_vm"])
    max_per_machine = str(kwargs["max_per_machine"])

    deployment_command = [
        commons.get_gs_script_path(),
        "deploy-space",
        "-cluster",
        "schema=" + schema + " total_members=" + partitions + "," + backups,
        "-max-instances-per-vm " + max_per_vm,
        "-max-instances-per-machine " + max_per_machine,
        grid_name
    ]

    commons.run_command(deployment_command, ctx)


@operation
def undeploy_grid(**kwargs):
    grid_name = kwargs["grid_name"]

    deployment_command = [
        commons.get_gs_script_path(),
        "undeploy",
        grid_name
    ]

    commons.run_command(deployment_command, ctx)


@operation
def deploy_pu(**kwargs):
    override_pu_name = kwargs["override_pu_name"]
    schema = kwargs["schema"]
    partitions = str(kwargs["partitions"])
    backups = str(kwargs["backups"])
    max_per_vm = str(kwargs["max_per_vm"])
    max_per_machine = str(kwargs["max_per_machine"])

    tmp_pus = '/tmp/pus'
    if not os.path.exists(tmp_pus):
        os.makedirs(tmp_pus)
    jar_name = kwargs["pu_url"].split("/")[-1]

    pu_location = tmp_pus + '/' + jar_name
    urllib.urlretrieve(kwargs["pu_url"], pu_location)
    if override_pu_name != {}:
        pu_name = override_pu_name
    else:
        pu_name = jar_name.split(".jar")[0]

    deployment_command = [
        commons.get_gs_script_path(),
        "deploy",
        "-cluster",
        "schema=" + schema + " total_members=" + partitions + "," + backups,
        "-max-instances-per-vm " + max_per_vm,
        "-max-instances-per-machine " + max_per_machine,
        "-override-name " + pu_name,
        pu_location
    ]

    commons.run_command(deployment_command, ctx)
