try:
    from setuptools import setup
except ImportError:
    from distutils import setup

config = {
    'description': 'Gothonweb Web App',
    'author': 'Chris Laws',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'christopherlaws85@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['gothonweb'],
    'scripts': [],
    'name' : 'gothonweb project'
}

setup(**config)