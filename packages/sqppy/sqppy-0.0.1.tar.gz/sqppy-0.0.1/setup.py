import  sys
from setuptools import setup,find_packages

with open("README.md","r") as f:
    desciption  =  f.read()

setup(
    name='SQLSadra',
    author="Sadr Farmani",
    version='1.0',
    packages=find_packages(),
    install_requires=[
        #numpy >=1.11.1
    ],
    entry_points={
        "console_scripts":[
            "SQLSadra =  SQLSadra:hello",
        ],
    },
    long_description=desciption,
    long_description_content_type = "text/markdown",

    project_urls  = {"Linkdin":"https://www.google.com"},





)