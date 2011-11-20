#### Introduction

This package is pythonic API to kinopoisk.ru website.

#### Example usage:

Search movies:

```
>>> from kinopoisk import Movie
>>> movie_list = Movie.objects.search('Redacted')
>>> len(movie_list)
1
>>> print movie_list[0].title
Без цензуры
```
#### Installation:

To install the latest version using pip:

```
$ pip install kinopoiskpy
```