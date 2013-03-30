# Kinopoiskpy

[![Build Status](https://travis-ci.org/ramusus/kinopoiskpy.png?branch=master)](https://travis-ci.org/ramusus/kinopoiskpy) [![Coverage Status](https://coveralls.io/repos/ramusus/kinopoiskpy/badge.png?branch=master)](https://coveralls.io/r/ramusus/kinopoiskpy)

This package is pythonic API to kinopoisk.ru website.

## Installation

To install the latest version using pip:

    $ pip install kinopoiskpy

## Example usage

Search movies:

    >>> from kinopoisk import Movie
    >>> movie_list = Movie.objects.search('Redacted')
    >>> len(movie_list)
    1
    >>> print movie_list[0].title
    Без цензуры

## Contributors

[Alex Rembish](http://github.com/rembish)