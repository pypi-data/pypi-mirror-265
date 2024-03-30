# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doy']

package_data = \
{'': ['*']}

install_requires = \
['filelock>=3.12.2,<4.0.0',
 'matplotlib>=3.6.2',
 'numpy',
 'rich>=13.4.1',
 'tqdm>=4.65.0',
 'wandb>=0.15.5']

setup_kwargs = {
    'name': 'doy',
    'version': '1.9.1',
    'description': '',
    'long_description': '# Doy\n\nSimple utility package\n',
    'author': 'Dominik Schmidt',
    'author_email': 'schmidtdominik30@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
