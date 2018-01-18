try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'modules for implementing shuangs game',
    'author': 'Shuang Li',
    'url': 'URL to get it at',
    'download_url': 'Where to download it',
    'author_email': 'lishuang2009@gmail.com',
    'version': '0.1',
    'install_requires': [],
    'packages': ['shuang_game'],
    'scripts': [],
    'name': 'shuang_game'
}

setup(**config)
