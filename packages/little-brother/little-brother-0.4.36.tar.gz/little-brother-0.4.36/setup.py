# -*- coding: utf-8 -*-

#    Copyright (C) 2019-2024  Marcus Rickert
#
#    See https://github.com/marcus67/little_brother
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from os import path

from setuptools import setup

import little_brother.settings

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'requirements.txt')) as f:
    install_requires = f.read().splitlines()

setup_params = {
    # standard setup configuration

    "install_requires": install_requires,

    "packages": ['little_brother',
                 'little_brother.api',
                 'little_brother.devices',
                 'little_brother.persistence',
                 'little_brother.web',
                 'little_brother.test',
                 'little_brother.test.persistence',
                 'little_brother.test.pytests.devices',
                 'little_brother.test.pytests',
                 'little_brother.test.web',
                 'little_brother.test.api',
                 ],

    "include_package_data": True,

    "scripts": [
        "run_little_brother.py",
        "run_little_brother_test_suite.py",
    ],
    "long_description": "Tool to monitor login time of users on Debian hosts and terminate processes if usage times "
                        "are exceeded. Note that this package is not meant as a simple install with PIP since it "
                        "also requires additional work in the operating system (e.g. add a user, create directories, "
                        "define a startup service). This is all done by the Debian package provided at "
                        "https://sourceforge.net/projects/little-brother/ .",
}

extended_setup_params = {

    # Target version to be used to upgrade the database
    "target_alembic_version": "8802c76063af",

    "docker_registry_user": "marcusrickert",
    # Docker image contexts to be built. The second entry of the tuple denotes if the resulting image is to be uploaded
    "docker_contexts": [ ('little-brother-base', False),
                         ('little-brother-client', True),
                         ('little-brother-ubuntu-base', False),
                         ('little-brother-ubuntu-client', True),
#                         ('little-brother-arch-linux-base', False),
#                         ('little-brother-arch-linux-client', True),
                         ('little-brother-alpine-client', True),
                         ],

    # additional setup configuration used by CI stages
    "owasp": True,

    # technical name used for e.g. directories, PIP-package, and users
    "create_user": True,
    "create_group": True,
    "user_group_mappings": [("little-brother", "audio")],
    "deploy_systemd_service": True,
    # "deploy_tmpfile_conf": True,
    "deploy_sudoers_file": True,
    "deploy_apparmor_file": True,
    "contributing_setups": [
        "python_base_app",
        "some_flask_helpers",
    ],
    "publish_debian_package": little_brother.settings.SOURCEFORGE_CHANNELS,
    "publish_docker_images": little_brother.settings.DOCKER_CHANNELS,
    "publish_latest_docker_image": little_brother.settings.RELEASE_BRANCH_NAME,
    "debian_extra_files": [
        ("etc/client.config", "etc/little-brother/client.config"),
        ("etc/master.config", "etc/little-brother/master.config"),
    ],
    "debian_templates": [
        ("/etc/little-brother/master.config", "/etc/little-brother/little-brother.config")
    ],
    "build_pypi_package": True,
    "publish_pypi_package": {
        little_brother.settings.RELEASE_BRANCH_NAME: ('PYPI_API_URL', 'PYPI_API_TOKEN', 'TEST_PYPI_API_USER'),
        little_brother.settings.MASTER_BRANCH_NAME: ('TEST_PYPI_API_URL', 'TEST_PYPI_API_TOKEN', 'TEST_PYPI_API_USER')
    },
    "generate_generic_install": True,
    "analyze": True,
    "analyze_extra_exclusions" : "vagrant/**",
    "script_timeout": 30,
}

setup_params.update(little_brother.settings.settings)
extended_setup_params.update(little_brother.settings.extended_settings)
extended_setup_params.update(setup_params)


if __name__ == '__main__':
    setup(**setup_params)
