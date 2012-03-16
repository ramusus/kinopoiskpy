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

    def __init__(self, **kwargs):
        super(Movie, self).__init__(**kwargs)
        from sources import MovieLink, MoviePremierLink, MovieMainPage, MoviePostersPage # import here for successful installing via pip
        self.register_source('link', MovieLink)
        self.register_source('premier_link', MoviePremierLink)
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