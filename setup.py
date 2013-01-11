from setuptools import setup, find_packages

setup(
    name='kinopoiskpy',
    version=__import__('kinopoisk').__version__,
    description='Python API to kinopoisk.ru',
    long_description=open('README.md').read(),
    author='ramusus',
    author_email='ramusus@gmail.com',
    url='https://github.com/ramusus/kinopoiskpy',
    download_url='http://pypi.python.org/pypi/kinopoiskpy',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False, # because we're including media that Django needs
    install_requires=[
        'beautifulsoup',
        'requests',
        'python-dateutil'
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
