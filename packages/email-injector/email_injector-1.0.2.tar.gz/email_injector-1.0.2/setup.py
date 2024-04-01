# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['email_injector']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'email-injector',
    'version': '1.0.2',
    'description': '',
    'long_description': '',
    'author': 'Antoni Oktha Fernandes',
    'author_email': '37358597+DesKaOne@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
