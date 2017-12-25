from setuptools import setup, find_packages
from io import open

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md', encoding='utf-8').read()

setup(
    name='kinopoiskpy',
    version=__import__('kinopoisk').__version__,
    description='Python API to kinopoisk.ru',
    long_description=long_description,
    author='ramusus',
    author_email='ramusus@gmail.com',
    url='https://github.com/ramusus/kinopoiskpy',
    download_url='http://pypi.python.org/pypi/kinopoiskpy',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,  # because we're including media that Django needs
    install_requires=[
        'beautifulsoup4',
        'lxml',
        'requests',
        'simplejson',
        'python-dateutil',
        'future',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='kinopoisk.tests',
)
