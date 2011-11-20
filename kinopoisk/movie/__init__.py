# -*- coding: utf-8 -*-
from kinopoisk.utils import KinopoiskObject, Manager

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

    posters = []

    def __init__(self, **kwargs):
        super(Movie, self).__init__(**kwargs)
        from sources import MovieLink, MovieMainPage, MoviePostersPage # import here for successful installing via pip
        self.register_source('link', MovieLink)
        self.register_source('main_page', MovieMainPage)
        self.register_source('posters', MoviePostersPage)
        self.posters = []
        self.audience = []

    def __repr__(self):
        return '%s (%s), %s' % (self.title, self.title_original, self.year)

    def get_posters(self):
        title = self.title.replace(' ', '-') if self.title else 'Title'
        return ['http://st3.kinopoisk.ru/im/poster/1/1/1/kinopoisk.ru-%s-%d.jpg' % (title, img_id) for img_id in self.posters]

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

Movie.objects = MovieManager()
