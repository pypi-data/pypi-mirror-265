# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['feynamp', 'feynamp.form', 'feynamp.sympy']

package_data = \
{'': ['*']}

install_requires = \
['feynml>=0.2.26', 'feynmodel>=0.0.5', 'python-form', 'sympy']

setup_kwargs = {
    'name': 'feynamp',
    'version': '0.0.5',
    'description': 'Compute Feynman diagrams',
    'long_description': '# FeynAmp\n\n\n## Related\n\n* Mathematica: FormCalc, FeynCalc\n* Julia: https://arxiv.org/pdf/2310.07634.pdf\n',
    'author': 'Alexander Puck Neuwirth',
    'author_email': 'alexander@neuwirth-informatik.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/APN-Pucky/feynamp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
