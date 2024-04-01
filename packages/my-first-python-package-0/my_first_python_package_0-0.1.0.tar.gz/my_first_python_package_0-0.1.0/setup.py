# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['my_first_python_package']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=8.1.1,<9.0.0']

setup_kwargs = {
    'name': 'my-first-python-package-0',
    'version': '0.1.0',
    'description': 'A simple package to demonstrate how to create a python package',
    'long_description': '# my-first-python-package',
    'author': 'Hassan Abedi',
    'author_email': 'hassan.abedi.t@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
