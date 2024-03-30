# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['benediction',
 'benediction._utils',
 'benediction.style',
 'benediction.style.color']

package_data = \
{'': ['*']}

extras_require = \
{':sys_platform == "windows"': ['windows-curses>=2.3.2,<3.0.0']}

setup_kwargs = {
    'name': 'benediction',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'austerj',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.12,<4.0',
}


setup(**setup_kwargs)
