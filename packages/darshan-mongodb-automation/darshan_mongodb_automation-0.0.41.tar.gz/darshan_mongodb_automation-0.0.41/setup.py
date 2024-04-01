from setuptools import setup, find_packages
from typing import List

def get_long_description(file_name:str)->str:
    with open(file_name, 'r', encoding = 'utf-8') as file_obj:
        long_description = file_obj.read()
    return long_description

HYPEN_E_DOT = '-e .'
def get_requirements(file_name:str):
    ''' returs the requirements project development environment '''
    with open(file_name, 'r') as file_obj:
        requirements = [requirement.replace('\n', '') for requirement in file_obj.readlines()]
    if HYPEN_E_DOT in requirements:
        requirements.remove(HYPEN_E_DOT)
    return requirements

PACKAGE_NAME = 'darshan_mongodb_automation'
VERSION = "0.0.41"
AUTHOR_USER_NAME = 'DarshanRM'
AUTHOR_EMAIL = 'darshanrokkad2003@gmail.com'
GITHUB_REPO_URL = 'https://github.com/DarshanRokkad/MongoDB_Connector_Package'

setup(
    name = PACKAGE_NAME,
    version = VERSION,
    author = AUTHOR_USER_NAME, 
    author_email = AUTHOR_EMAIL,

    description = 'A python package for connecting to mongodb',
    long_description = get_long_description('README.md'),
    long_description_content_type = 'text/markdown',

    url = GITHUB_REPO_URL,
    project_urls = {
        'Bug Tracker' : f'{GITHUB_REPO_URL}/issues'
    },

    package_dir = {'' : 'src'},
    packages = find_packages(where = 'src'),
    
    # install_requires = get_requirements('requirements_dev.txt')
    install_requires = ['pymongo', 'pymongo[srv]', 'dnspython', 'pandas', 'numpy', 'ensure', 'pytest', 'tox', 'black', 'flake8', 'mypy']
)