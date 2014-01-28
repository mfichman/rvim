from setuptools import setup

setup(
    name = 'rvim',
    version = '0.0.1',
    author = 'Matt Fichman',
    author_email = 'matt.fichman@gmail.com',
    description = ('Remote VIM-integrated fileserver and client'),
    license = 'MIT',
    keywords = ('vim', 'remote'),
    url = '',
    packages = ['rvim'],
    requires = ('bottle', 'gevent', 'watchdog'),
    entry_points = {
        'console_scripts': (
            'rvim = rvim.cli:main',
            'rvim-client = rvim.client:main',
            'rvim-server = rvim.server:main',
        )
    }
)
