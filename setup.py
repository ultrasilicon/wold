import os
from setuptools import setup, find_packages


setup(
    name = "wold",
    version = "0.0.1",
    author = "Tim Zheng",
    author_email = "zhenghanecho@gmail.com",
    description = ("YAML configed WoL daemon that wakes up boxes from Internet without DDNS"),
    license = "GPLv3",
    keywords = "WoL",
    url = "https://github.com/ultrasilicon/wold",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        "Topic :: Utilities",
    ],
    install_requires=[
          'ruamel.yaml',
          'simplejson',
          'typer',
          'websockets'
    ],
    entry_points={
        'console_scripts': [
            'wold = wold.app:main',
        ],
    }
)