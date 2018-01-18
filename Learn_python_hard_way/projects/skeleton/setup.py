try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'My project',
    'author': 'My Name',
    'url': 'URL to get it at',
    'download_url': 'Where to download it',
    'author_email': 'My email',
    'version': '0.1',
    'install_requires': ['noise'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'projectname'
}

setup(**config)
