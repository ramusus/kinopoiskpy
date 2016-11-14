# Kinopoiskpy

[![Build Status](https://travis-ci.org/ramusus/kinopoiskpy.png?branch=master)](https://travis-ci.org/ramusus/kinopoiskpy) [![PyPI version](https://badge.fury.io/py/kinopoiskpy.png)](http://badge.fury.io/py/kinopoiskpy) [![Coverage Status](https://coveralls.io/repos/ramusus/kinopoiskpy/badge.png?branch=master)](https://coveralls.io/r/ramusus/kinopoiskpy)

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

Get content of movie by ID:

    >>> from kinopoisk.movie import Movie
    >>> movie = Movie(id=278229)
    >>> movie.get_content('main_page')
    >>> movie.year
    2007
    >>> movie.title
    u'Без цензуры'
    >>> movie.title_original
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
    >>> movie.__dict__.keys()
    ['rating', 'series', 'seasons', 'year', '_sources', 'id', 'composers', 'plot', 'genres', 'title', 'tagline', 'profit_usa', 'audience', 'scenarios', 'profit_russia', 'operators', 'youtube_ids', 'trailers', 'posters', 'producers', 'countries', 'budget', 'title_original', 'directors', 'release', 'runtime']

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
    >>> person.name_original
    u'Johnny Depp'
    >>> len(person.information) > 50
    True
    >>> person.get_content('photos')
    >>> len(person.photos) > 10
    True
    >>> person.__dict__.keys()
    ['information', 'name', 'name_original', 'photos', '_sources', 'id', 'year_birth']

## Contributors

[Alex Rembish](http://github.com/rembish)
