# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['majormode',
 'majormode.tendkid',
 'majormode.tendkid.constant',
 'majormode.tendkid.model']

package_data = \
{'': ['*']}

install_requires = \
['perseus-core-library>=1.20.3,<2.0.0']

setup_kwargs = {
    'name': 'tendkid-core-library',
    'version': '1.0.0',
    'description': 'Collection of reusable Python components to share with Python projects integrating TendKid',
    'long_description': '# TendKid Core Python Library\nCollection of reusable Python components to share with Python projects integrating TendKid.\n',
    'author': 'Daniel CAUNE',
    'author_email': 'daniel.caune@tendkid.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tendkid/library_tendkid-core_python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
