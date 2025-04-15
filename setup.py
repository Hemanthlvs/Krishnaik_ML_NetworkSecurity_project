from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    try:
        requirements_list:List[str] = []
        with open ('requirements.txt') as file:
            lines = file.readlines()
            for line in lines:
                requirement = lines.strip()
                if requirement and requirement != '-e .':
                    requirements_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirements_list

setup(
    name='NetworkSecurity',
    version='0.0.1',
    author='Hemanth LVS',
    author_email='lvshemanth@gmail.com',
    packages=find_packages(),
    install_requirements = get_requirements()
)