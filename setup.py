import os
from setuptools import setup, find_packages


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__),
                                       os.pardir)))

requirements = [
    'django>=1.5',
]

extras_require = {
    'test': ['coverage', 'selenium'],
}

setup(
    name='django-jchart',
    version='0.3.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    license='BSD License',
    description='A Django App to plot charts using the excellent Chart.JS library.',
    long_description=README,
    url='https://github.com/matthisk/django-jchart',
    author='Matthisk Heimensen',
    author_email='m@tthisk.nl',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
