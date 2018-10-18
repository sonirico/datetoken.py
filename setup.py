import io
import re
from collections import OrderedDict

from setuptools import setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('datetoken/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='datetoken',
    version=version,
    url='https://pypi.org/project/datetoken/',
    project_urls=OrderedDict((
        ('Code', 'https://github.com/sonirico/datetoken/'),
        ('Issue tracker', 'https://github.com/sonirico/datetoken/issues'),
    )),
    license='MIT',
    author='Marcos Sanchez',
    author_email='marsanben92@gmail.com',
    maintainer='Marcos Sanchez',
    maintainer_email='marsanben92@gmail.com',
    description='Convert relative string tokens into datetime objects',
    long_description=readme,
    packages=['datetoken'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    install_requires=[
        'pytz==2018.04',
        'python-dateutil==2.7.3'
    ],
    extras_require={
        'dev': [
            'pytest>=3',
            'coverage',
            'tox',
        ],
        'docs': [
        ]
    },
)
