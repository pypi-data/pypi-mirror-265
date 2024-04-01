# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['google_injector',
 'google_injector.base',
 'google_injector.exc',
 'google_injector.fire',
 'google_injector.response',
 'google_injector.utils']

package_data = \
{'': ['*']}

install_requires = \
['gcloud>=0.18.3,<0.19.0',
 'http-injector>=1.0.1,<2.0.0',
 'oauth2client>=4.1.3,<5.0.0',
 'pycryptodomex>=3.20.0,<4.0.0',
 'python-dotenv>=1.0.1,<2.0.0',
 'python-jwt>=4.1.0,<5.0.0',
 'sqlalchemy-utils>=0.41.2,<0.42.0',
 'sqlalchemy>=2.0.29,<3.0.0']

setup_kwargs = {
    'name': 'google-injector',
    'version': '1.0.3',
    'description': '',
    'long_description': 'pip install google_injector',
    'author': 'Antoni Oktha Fernandes',
    'author_email': '37358597+DesKaOne@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
