# -*- coding: utf-8 -*-
from utils import KinopoiskObject, KinopoiskPage, Manager
import re
import sys

class MovieLink(KinopoiskPage):
    '''
    Class for parsing movie info from links
    '''
    def parse_link(self, content):
        '''
        >>> m = Movie()
        >>> m.parse_link(u'<td width=100% class="news"><a class="all" href="/level/1/film/179805/">Title</a>,&nbsp;<a href="/level/10/m_act[year]/1952/" class=orange>1952</a></td></tr><tr><td></td><td><i class="search_rating"></i><font color="#999999">... 10 Days in a Nudist Camp</font></td>')
        >>> m.title
        u'Title'
        >>> m.id
        179805
        >>> m.year
        1952
        >>> m.title_original
        u'10 Days in a Nudist Camp'

        >>> m = Movie()
        >>> m.parse_link(u'<td width=95% align=left class="news"><a class="all" href="/level/1/film/36620/sr/1">Title</a>,&nbsp;<a href="/level/10/m_act[year]/1991/" class="continue">1991</a></td> </tr> <tr><td></td><td><i class="search_rating">5.867</i><font color="#999999">100 Days</font><product></td>')
        >>> m.title
        u'Title'
        >>> m.id
        36620
        >>> m.year
        1991
        >>> m.title_original
        u'100 Days'
        '''
        link = re.compile(r'<a class="all" href="/level/1/film/(\d+)/[^"]*">(.+?)</a>').findall(content)
        if link:
            self.id = self.prepare_int(link[0][0])
            self.title = self.prepare_str(link[0][1])

        year = re.compile(r'<a href="/level/10/m_act\[year\]/(\d{4})/"').findall(content)
        if year:
            self.year = self.prepare_int(year[0])

        otitle = re.compile(r'<font color="#999999">(.+?)</font>').findall(content)
        if otitle:
            self.title_original = self.prepare_str(re.sub(r'^\.\.\. ', '', otitle[0]))

        self.set_source('link')

class MovieMainPage(KinopoiskPage):
    '''
    Class for parsing main movie page purpose
    '''
    def __init__(self):
        self.set_url('main_page', '/level/1/film/%d/')

    def parse_main_page(self, content):
        '''
        >>> m = Movie()
        >>> m.parse_main_page(u'<h1 style="margin: 0; padding: 0" class="moviename-big">Title</h1><span class="_reachbanner_">Description</span>')
        >>> m.title
        u'Title'
        >>> m.plot
        u'Description'
        '''
        title = re.compile(r'<h1 style="margin: 0; padding: 0" class="moviename-big">(.+?)</h1>').findall(content)
        if title:
            self.title = self.prepare_str(title[0])

        title_original = re.compile(r'<span style="color: #666; font-size: 13px">(.+?)</span>').findall(content)
        if title_original:
            self.title_original = self.prepare_str(title_original[0])

        plot = re.compile(r'<span class="_reachbanner_">(.+?)</span>').findall(content)
        if plot != []:
            self.plot = self.prepare_str(plot[0])

        content_info = content[content.find(u'<!-- инфа о фильме -->'):content.find(u'<!-- /инфа о фильме -->')]
        content_info = re.compile(r'<tr><td class="type">(.+?)</td><td[^>]*>(.+?)</td></tr>').findall(content_info)
        for name, value in content_info:
            if name == u'слоган':
                self.tagline = self.prepare_str(value)
            elif name == u'время':
                self.runtime = self.prepare_str(value)

        self.set_source('main_page')

class Movie(KinopoiskObject, MovieLink, MovieMainPage):

    title = None
    title_original = None
    plot = ''

    year = None
    countries = []
    tagline = None

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

    def __repr__(self):
        return '%s (%s), %s' % (self.title, self.title_original, self.year)

class MovieManager(Manager):
    '''
    >>> m = Movie.objects.search('Redacted')[0]
    >>> m.title
    u'\u0411\u0435\u0437 \u0446\u0435\u043d\u0437\u0443\u0440\u044b'
    >>> m.title_original
    u'Redacted'
    >>> m.plot
    u'\u0412 \u0446\u0435\u043d\u0442\u0440\u0435 \u043a\u0430\u0440\u0442\u0438\u043d\u044b  -  \u043d\u0435\u0431\u043e\u043b\u044c\u0448\u043e\u0439 \u043e\u0442\u0440\u044f\u0434 \u0430\u043c\u0435\u0440\u0438\u043a\u0430\u043d\u0441\u043a\u0438\u0445 \u0441\u043e\u043b\u0434\u0430\u0442 \u043d\u0430 \u043a\u043e\u043d\u0442\u0440\u043e\u043b\u044c\u043d\u043e-\u043f\u0440\u043e\u043f\u0443\u0441\u043a\u043d\u043e\u043c \u043f\u0443\u043d\u043a\u0442\u0435 \u0432 \u0418\u0440\u0430\u043a\u0435. \u041f\u0440\u0438\u0447\u0451\u043c \u0432\u043e\u0441\u043f\u0440\u0438\u044f\u0442\u0438\u0435 \u0438\u0445 \u0438\u0441\u0442\u043e\u0440\u0438\u0438 \u043f\u043e\u0441\u0442\u043e\u044f\u043d\u043d\u043e \u043c\u0435\u043d\u044f\u0435\u0442\u0441\u044f. \u041c\u044b \u0432\u0438\u0434\u0438\u043c \u0441\u043e\u0431\u044b\u0442\u0438\u044f \u0433\u043b\u0430\u0437\u0430\u043c\u0438 \u0441\u0430\u043c\u0438\u0445 \u0441\u043e\u043b\u0434\u0430\u0442, \u043f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u0438\u0442\u0435\u043b\u0435\u0439 \u0421\u041c\u0418, \u0438\u0440\u0430\u043a\u0446\u0435\u0432, \u0438 \u043f\u043e\u043d\u0438\u043c\u0430\u0435\u043c, \u043a\u0430\u043a \u043d\u0430 \u043a\u0430\u0436\u0434\u043e\u0433\u043e \u0438\u0437 \u043d\u0438\u0445 \u0432\u043b\u0438\u044f\u0435\u0442 \u043f\u0440\u043e\u0438\u0441\u0445\u043e\u0434\u044f\u0449\u0435\u0435, \u0438\u0445 \u0432\u0441\u0442\u0440\u0435\u0447\u0438 \u0438 \u0441\u0442\u043e\u043b\u043a\u043d\u043e\u0432\u0435\u043d\u0438\u044f \u0434\u0440\u0443\u0433 \u0441 \u0434\u0440\u0443\u0433\u043e\u043c.'
    >>> m.runtime
    u'90 \u043c\u0438\u043d.'
    >>> m.tagline
    u'"\u0424\u0438\u043b\u044c\u043c, \u0437\u0430\u043f\u0440\u0435\u0449\u0435\u043d\u043d\u044b\u0439 \u043a \u043f\u0440\u043e\u043a\u0430\u0442\u0443 \u0432\u043e \u043c\u043d\u043e\u0433\u0438\u0445 \u0441\u0442\u0440\u0430\u043d\u0430\u0445"'

    >>> movies = Movie.objects.search('pulp fiction')
    >>> len(movies) > 1
    True
    >>> m = movies[0]
    >>> m.title
    u'\u041a\u0440\u0438\u043c\u0438\u043d\u0430\u043b\u044c\u043d\u043e\u0435 \u0447\u0442\u0438\u0432\u043e'
    >>> m.year
    1994
    >>> m.title_original
    u'Pulp Fiction'
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

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)