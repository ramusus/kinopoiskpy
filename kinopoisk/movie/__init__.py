# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from future.utils import python_2_unicode_compatible

from .sources import MovieLink, MoviePremierLink, MovieMainPage, MoviePostersPage, MovieTrailersPage, MovieSeries
from ..utils import KinopoiskObject, Manager, get_request


@python_2_unicode_compatible
class Movie(KinopoiskObject):
    def set_defaults(self):
        self.title = ''
        self.title_original = ''
        self.plot = ''

        self.year = None
        self.countries = []
        self.tagline = ''

        self.actors = []
        self.directors = []
        self.scenarios = []
        self.producers = []
        self.operators = []
        self.composers = []
        self.genres = []

        self.budget = None
        self.profit_usa = None
        self.profit_russia = None
        self.profit_world = None
        self.audience = []

        self.rating = None
        self.runtime = None
        self.release = None

        self.posters = []
        self.trailers = []
        self.youtube_ids = []

        self.series = None
        self.seasons = []

    def __init__(self, *args, **kwargs):
        super(Movie, self).__init__(*args, **kwargs)

        self.register_source('link', MovieLink)
        self.register_source('premier_link', MoviePremierLink)
        self.register_source('main_page', MovieMainPage)
        self.register_source('posters', MoviePostersPage)
        self.register_source('trailers', MovieTrailersPage)
        self.register_source('series', MovieSeries)

    def __repr__(self):
        return '%s (%s), %s' % (self.title, self.title_original, self.year or '-')

    def add_trailer(self, trailer_params):
        trailer = Trailer(trailer_params)
        if trailer.is_valid and trailer.id not in [tr.id for tr in self.trailers]:
            self.trailers.append(trailer)

    def add_series_season(self, year, episodes):
        self.seasons.append(SeriesSeason(year, [SeriesEpisode(title, date) for title, date in episodes]))


@python_2_unicode_compatible
class Trailer(object):
    def set_defaults(self):
        self.id = None
        self.width = None
        self.heigth = None
        self.file = None
        self.dom = 'tr'
        self.advsys = 'rutube'
        self.sbt = ''
        self.genres = None
        self.preview_file = None
        self.preview_width = None
        self.preview_heigth = None

    def __init__(self, params=None):
        self.set_defaults()

        if params:
            self.id = params['trailerId'].replace('top', '')
            self.width = params['trailerW']
            self.heigth = params['trailerH']
            self.file = params['trailerFile']
            self.dom = params['trailerDom']
            self.advsys = params['trailerAdvsys']
            self.sbt = params['trailerSbt']
            self.genres = params['genres']
            self.preview_file = params['previewFile']
            self.preview_width = params['previewW']
            self.preview_heigth = params['previewH']

    @property
    def is_valid(self):
        '''
        Check if filename is correct
        '''
        # not youtube video '521689/' (http://www.kinopoisk.ru/film/521689/video/)
        return self.file[-1] != '/'


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
        return '%s, %s' % (self.title if self.title else '???', self.release_date or '-')


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
        return '%d: %d' % (self.year, len(self.episodes))


class MovieManager(Manager):
    '''
    Movie manager
    '''
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
        response = get_request(url, params=params)
        content = response.content.decode('windows-1251', 'ignore')

        content_soup = BeautifulSoup(content, 'lxml')
        instances = []
        for premier in content_soup.findAll('div', {'class': 'premier_item'}):
            instance = self.kinopoisk_object()
            instance.parse('premier_link', premier)
            instances += [instance]

        return instances


Movie.objects = MovieManager()
Movie.premiers = MoviePremiersManager()
