# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_learning_standards']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pylearningstandards',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Daniel Auerbach',
    'author_email': 'auerbach@ict.usc.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
