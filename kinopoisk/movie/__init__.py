# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from future.utils import python_2_unicode_compatible
from bs4 import BeautifulSoup

from .sources import (
    MovieLink, MoviePremierLink, MovieMainPage, MoviePostersPage, MovieTrailersPage, MovieSeries, MovieCareerLink,
    MovieCastPage, MovieRoleLink)
from ..utils import KinopoiskObject, Manager


@python_2_unicode_compatible
class Movie(KinopoiskObject):
    """
    Movie Class
    """
    def set_defaults(self):
        self.title = ''
        self.title_en = ''
        self.plot = ''

        self.year = None
        self.countries = []
        self.tagline = ''

        self.actors = []
        self.directors = []
        self.screenwriters = []
        self.producers = []
        self.operators = []
        self.composers = []
        self.art_direction_by = []
        self.editing_by = []
        self.genres = []
        self.cast = {}

        self.budget = None
        self.marketing = None
        self.profit_usa = None
        self.profit_russia = None
        self.profit_world = None
        self.audience = []

        self.rating = None
        self.votes = None
        self.imdb_rating = None
        self.imdb_votes = None
        self.runtime = None
        self.release = None

        self.posters = []
        self.trailers = []
        self.youtube_ids = []

        self.series = None
        self.series_years = tuple()
        self.seasons = []

    def __init__(self, *args, **kwargs):
        super(Movie, self).__init__(*args, **kwargs)

        self.register_source('link', MovieLink)
        self.register_source('premier_link', MoviePremierLink)
        self.register_source('career_link', MovieCareerLink)
        self.register_source('main_page', MovieMainPage)
        self.register_source('cast', MovieCastPage)
        self.register_source('posters', MoviePostersPage)
        self.register_source('trailers', MovieTrailersPage)
        self.register_source('series', MovieSeries)

    def __repr__(self):
        return '{} ({}), {}'.format(self.title, self.title_en, self.year or '-')

    def add_trailer(self, trailer_id):
        trailer = Trailer(trailer_id)
        if trailer.is_valid and trailer.id not in [tr.id for tr in self.trailers]:
            self.trailers.append(trailer)

    def add_series_season(self, year, episodes):
        self.seasons.append(SeriesSeason(year, [SeriesEpisode(title, date) for title, date in episodes]))


@python_2_unicode_compatible
class Role(KinopoiskObject):
    """
    Movie Role Class
    """
    def set_defaults(self):
        self.name = ''
        self.person = None
        self.voice = False

    def __init__(self, *args, **kwargs):
        super(Role, self).__init__(*args, **kwargs)

        self.register_source('role_link', MovieRoleLink)


@python_2_unicode_compatible
class Trailer(object):
    """
    Movie Trailer Class
    """
    def set_defaults(self):
        self.id = None

    def __init__(self, id):
        self.set_defaults()
        if id:
            self.id = id

    @property
    def is_valid(self):
        """
        Check if filename is correct
        """
        # not youtube video '521689/' (http://www.kinopoisk.ru/film/521689/video/)
        return self.file[-1] != '/'

    @property
    def file(self):
        trailer_file = 'gettrailer.php?quality=hd&trailer_id={}'.format(self.id)
        return trailer_file


@python_2_unicode_compatible
class SeriesEpisode(object):
    def set_defaults(self):
        self.title = ''
        self.release_date = None

    def __init__(self, title=None, release_date=None):
        self.set_defaults()

        self.title = title
        self.release_date = release_date

    def __repr__(self):
        return '{}, {}'.format(self.title if self.title else '???', self.release_date or '-')


@python_2_unicode_compatible
class SeriesSeason(object):
    def set_defaults(self):
        self.year = None
        self.episodes = []

    def __init__(self, year, episodes=None):
        self.set_defaults()

        self.year = year
        if episodes:
            self.episodes = episodes

    def __repr__(self):
        return '{}: {}'.format(self.year, len(self.episodes))


class MovieManager(Manager):
    """
    Movie manager
    """
    kinopoisk_object = Movie

    def get_url_with_params(self, query):
        # http://www.kinopoisk.ru/index.php?level=7&from=forma&result=adv&m_act[from]=forma&m_act[what]=content&m_act[find]=pulp+fiction
        return ('http://www.kinopoisk.ru/index.php', {
            'level': 7,
            'from': 'forma',
            'result': 'adv',
            'm_act[from]': 'forma',
            'm_act[what]': 'content',
            'm_act[find]': query,
        })
        # возвращает не по релевантности, а непонятно как
        # http://www.kinopoisk.ru/index.php?level=7&ser=a:3:{s:4:"find";s:3:"day";s:4:"what";s:7:"content";s:5:"count";a:1:{s:7:"content";s:3:"113";}}&show=all
        # return ('http://www.kinopoisk.ru/index.php', {
        #     'level': 7,
        #     'ser': 'a:3:{s:4:"find";s:%d:"%s";s:4:"what";s:7:"content";s:5:"count";a:1:{s:7:"content";s:3:"113";}}' % (
        #         len(query), query),
        #     'show': 'all',
        # })


class MoviePremiersManager(Manager):
    kinopoisk_object = Movie

    def get_url_with_params(self, query=None):
        return 'http://www.kinopoisk.ru/level/8/view/prem/', {}

    def all(self):
        url, params = self.get_url_with_params()
        content = self.request.get_content(url, params=params)

        content_soup = BeautifulSoup(content, 'html.parser')
        instances = []
        for premier in content_soup.findAll('div', {'class': 'premier_item'}):
            instance = self.kinopoisk_object.get_parsed('premier_link', premier)
            instances += [instance]

        return instances


Movie.objects = MovieManager()
Movie.premiers = MoviePremiersManager()
