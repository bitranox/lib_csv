# single point for all configuration of the project

# stdlib
from setuptools import find_packages  # type: ignore
from typing import List, Dict

package_name = 'lib_csv'  # type: str
version = '0.1.0'
# codeclimate_link_hash - get it under https://codeclimate.com/github/<user>/<project>/badges
codeclimate_link_hash = '7fa21a0ced3820c5faa9'  # for lib_csv

# cc_test_reporter_id - get it under https://codeclimate.com/github/<user>/<project> and press "test coverage"
cc_test_reporter_id = 'b05edc2186d0eb19346f06fba788b9640156ed90ff13c05c97ae825f7a2f7134'    # for lib_csv

# pypi_password
# to create the secret :
# cd /<repository>
# travis encrypt -r bitranox/lib_parameter pypi_password=*****
# copy and paste the encrypted password here
# replace with:
# travis_pypi_secure_code = '<code>'     # pypi secure password, without '"'
travis_pypi_secure_code = ''             # pypi secure password

# include package data files
# package_data = {package_name: ['some_file_to_include.txt']}
package_data = dict()       # type: Dict[str, List[str]]

author = 'Robert Nowotny'
author_email = 'rnowotny1966@gmail.com'
github_account = 'bitranox'

linux_tests = True
osx_tests = True
pypy_tests = True
windows_tests = True
wine_tests = False
badges_with_jupiter = False

# a short description of the Package - especially if You deploy on PyPi !
description = package_name + ': functions to read and write csv files'  # short description - should be entered here

# #############################################################################################################################################################
# DEFAULT SETTINGS - no need to change usually, but can be adopted
# #############################################################################################################################################################

shell_command = package_name
src_dir = package_name
module_name = package_name
init_config_title = description
init_config_name = package_name

# we ned to have a function main_commandline in module module_name - see examples
entry_points = {'console_scripts': ['{shell_command} = {src_dir}.{module_name}:main_commandline'
                .format(shell_command=shell_command, src_dir=src_dir, module_name=module_name)]}  # type: Dict[str, List[str]]

long_description = package_name  # will be overwritten with the content of README.rst if exists

packages = [package_name]

url = 'https://github.com/{github_account}/{package_name}'.format(github_account=github_account, package_name=package_name)
github_master = 'git+https://github.com/{github_account}/{package_name}.git'.format(github_account=github_account, package_name=package_name)
travis_repo_slug = github_account + '/' + package_name

CLASSIFIERS = ['Development Status :: 5 - Production/Stable',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: MIT License',
               'Natural Language :: English',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Topic :: Software Development :: Libraries :: Python Modules']
