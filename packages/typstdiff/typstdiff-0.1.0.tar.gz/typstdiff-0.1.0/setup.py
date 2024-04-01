# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typstdiff']

package_data = \
{'': ['*']}

install_requires = \
['pandoc>=2.3,<3.0', 'typst>=0.11.0,<0.12.0']

setup_kwargs = {
    'name': 'typstdiff',
    'version': '0.1.0',
    'description': 'Tool made with Pandoc to compare two files with typst extension.',
    'long_description': '# TypstDiff\n### Dominika Ferfecka, Sara Fojt, Małgorzata Kozłowska\n\n## Introduction\nTool created with Pandoc to compare two typst files. It marks things\ndeleted from first file and marks differently things added to the second file.\n\n## Run virtual environment\nTo run virtual environment in poetry go to TypstDiff folder and use command\n`poetry shell`\n\nTo exit virtual environment use command\n`exit`\n\n## Installing dependencies\nTo install the same versions of dependencies as used in the project you can use \n`pip install -e .` or `poetry install`\n\n## Run tests\nTo run tests use command\n`poetry run pytest -v`\n\n### Issues\nAs both tools - Pandoc and Typst are new and still developing there is no full support\nfor typst in Pandoc. Because of that it is not possible to notice all changes made\nin files, but tool will be developed.',
    'author': 'Sara Fojt',
    'author_email': '01169167@pw.edu.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
