import os

from setuptools import find_packages, setup


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

with open(os.path.join(os.path.dirname(__file__),
                       'django_auto_mutations/VERSION')) as version:
    VERSION = version.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-auto-mutations',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Auto generate gql mutations for your models using graphene',
    long_description=README,
    url='https://github.com/jsep/django-auto-mutations',
    author='Juan Sepulveda',
    author_email='juan@sepulveda.do',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
