# -*- coding: utf-8 -*-
from kinopoisk.utils import KinopoiskObject, Manager, get_request

class Movie(KinopoiskObject):

    title = ''
    title_original = ''
    plot = ''

    year = None
    countries = []
    tagline = ''

    directors = []
    scenarios = []
    producers = []
    operators = []
    composers = []
    genres = []

    budget = None
    profit_usa = None
    profit_russia = None
    audience = []

    rating = None
    runtime = None
    release = None

    posters = []
    trailers = []

    def __init__(self, *args, **kwargs):
        super(Movie, self).__init__(*args, **kwargs)
        from sources import MovieLink, MoviePremierLink, MovieMainPage, MoviePostersPage, MovieTrailersPage, MovieSeries # import here for successful installing via pip
        self.register_source('link', MovieLink)
        self.register_source('premier_link', MoviePremierLink)
        self.register_source('main_page', MovieMainPage)
        self.register_source('posters', MoviePostersPage)
        self.register_source('trailers', MovieTrailersPage)
        self.register_source('series', MovieSeries)
        self.posters = []
        self.trailers = []
        self.audience = []

        self.series = None
        self.seasons = []

    def __repr__(self):
        return ('<%s (%s), %s>' % (self.title, self.title_original, self.year or '-')).encode('utf-8')

    def get_posters(self):
        return self.posters

    def add_trailer(self, trailer_params):
        trailer = Trailer(trailer_params)
        if trailer.id not in [tr.id for tr in self.trailers]:
            self.trailers += [trailer]

class Trailer(object):
    id = None
    width = None
    heigth = None
    file = None
    dom = 'tr'
    advsys = "rutube"
    sbt = ""
    genres = None
    preview_file = None
    preview_width = None
    preview_heigth = None

    def __init__(self, params):
        self.id = params['trailerId'].replace('top','')
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
        return ('http://www.kinopoisk.ru/index.php', {
            'level': 7,
            'ser': 'a:3:{s:4:"find";s:%d:"%s";s:4:"what";s:7:"content";s:5:"count";a:1:{s:7:"content";s:3:"113";}}' % (len(query), query),
            'show': 'all',
        })

class MoviePremiersManager(Manager):

    kinopoisk_object = Movie

    def get_url_with_params(self):
        return ('http://www.kinopoisk.ru/level/8/view/prem/', {})

    def all(self):
        from BeautifulSoup import BeautifulSoup

        url, params = self.get_url_with_params()
        response = get_request(url, params=params)
        content = response.content.decode('windows-1251', 'ignore')

        content_soup = BeautifulSoup(content)
        instances = []
        for premier in content_soup.findAll('div', {'class': 'premier_item'}):
            instance = self.kinopoisk_object()
            instance.parse('premier_link', premier)
            instances += [instance]

        return instances

Movie.objects = MovieManager()
Movie.premiers = MoviePremiersManager()
