# Kinopoiskpy

[![PyPI version](https://img.shields.io/pypi/v/kinopoiskpy.svg)](https://pypi.python.org/pypi/kinopoiskpy) 
[![Circle CI](https://circleci.com/gh/ramusus/kinopoiskpy/tree/master.svg?style=shield)](https://circleci.com/gh/ramusus/kinopoiskpy)
[![Coverage Status](https://coveralls.io/repos/ramusus/kinopoiskpy/badge.svg?branch=master)](https://coveralls.io/r/ramusus/kinopoiskpy)
[![Build Status](https://img.shields.io/travis/ramusus/kinopoiskpy.svg?branch=master)](https://travis-ci.org/ramusus/kinopoiskpy) [![Coverage Status](https://coveralls.io/repos/ramusus/kinopoiskpy/badge.svg?branch=master)](https://coveralls.io/r/ramusus/kinopoiskpy)

This package is pythonic API to kinopoisk.ru website.

## Installation

To install the latest version using pip:

    $ pip install kinopoiskpy

## Example usage

Search movies:

    >>> from kinopoisk.movie import Movie
    >>> movie_list = Movie.objects.search('Redacted')
    >>> len(movie_list)
    1
    >>> print movie_list[0].title
    Без цензуры
    >>> print movie_list[0].id
    278229

Get content of movie by ID:

    >>> from kinopoisk.movie import Movie
    >>> movie = Movie(id=278229)
    >>> movie.get_content('main_page')
    >>> movie.year
    2007
    >>> movie.title
    u'Без цензуры'
    >>> movie.title_en
    u'Redacted'
    >>> movie.plot
    u'В центре картины  -  небольшой отряд американских солдат на контрольно-пропускном пункте в Ираке. Причём восприятие их истории постоянно меняется. Мы видим события глазами самих солдат, представителей СМИ, иракцев и понимаем, как на каждого из них влияет происходящее, их встречи и столкновения друг с другом.'
    >>> movie.runtime
    90
    >>> movie.tagline
    u'"Фильм, запрещенный к прокату во многих странах"'
    >>> movie.rating
    8.5
    >>> movie.get_content('posters')
    >>> len(movie.posters) > 0
    True

Get content of person by ID:

    >>> from kinopoisk.person import Person
    >>> person = Person(id=6245)
    >>> person.get_content('main_page')
    >>> person.id
    6245
    >>> person.name
    u'Джонни Депп'
    >>> person.year_birth
    1963
    >>> person.name_en
    u'Johnny Depp'
    >>> len(person.information) > 50
    True
    >>> person.get_content('photos')
    >>> len(person.photos) > 10
    True

## Testing

By default, all communication with kinopoisk.ru is recorded in special files called cassettes (see vcrpy-unittest). To reproduce real requests to kinopoisk.ru just delete directory `kinopoisk/tests/cassettes/` with all it's content.

Run all tests:

    $ python -W ignore -m kinopoisk.tests

Run particular test:

    $ python -W ignore -m kinopoisk.tests -v MovieTest.test_movie_cast

## Contributors

[Alex Rembish](http://github.com/rembish)
