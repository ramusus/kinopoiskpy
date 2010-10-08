# -*- coding: utf-8 -*-
from utils import KinopoiskObject, KinopoiskPage, Manager
from parser import UrlRequest
from BeautifulSoup import BeautifulSoup
import re
import sys

class MovieLink(KinopoiskPage):
    '''
    Class for parsing movie info from links
    '''
    def parse(self, object, content):
        '''
        >>> m = Movie()
        >>> m.parse('link', u'<td width=100% class="news"><a class="all" href="/level/1/film/179805/">Title</a>,&nbsp;<a href="/level/10/m_act[year]/1952/" class=orange>1952</a></td></tr><tr><td></td><td><i class="search_rating"></i><font color="#999999">... 10 Days in a Nudist Camp</font></td>')
        >>> m.title
        u'Title'
        >>> m.id
        179805
        >>> m.year
        1952
        >>> m.title_original
        u'10 Days in a Nudist Camp'

        >>> m = Movie()
        >>> m.parse('link', u'<td width=95% align=left class="news"><a class="all" href="/level/1/film/36620/sr/1">Title</a>,&nbsp;<a href="/level/10/m_act[year]/1991/" class="continue">1991</a></td> </tr> <tr><td></td><td><i class="search_rating">5.867</i><font color="#999999">100 Days</font><product></td>')
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
            object.id = self.prepare_int(link[0][0])
            object.title = self.prepare_str(link[0][1])

        year = re.compile(r'<a href="/level/10/m_act\[year\]/(\d{4})/"').findall(content)
        if year:
            object.year = self.prepare_int(year[0])

        otitle = re.compile(r'<font color="#999999">(.+?)</font>').findall(content)
        if otitle:
            object.title_original = self.prepare_str(re.sub(r'^\.\.\. ', '', otitle[0]))

        object.set_source('link')

class MovieMainPage(KinopoiskPage):
    '''
    Class for parsing main movie page purpose
    '''
    url = '/level/1/film/%d/'

    def parse(self, object, content):
        '''
        >>> m = Movie()
        >>> m.parse('main_page', u'<h1 style="margin: 0; padding: 0" class="moviename-big">Title</h1><span class="_reachbanner_">Description</span>')
        >>> m.title
        u'Title'
        >>> m.plot
        u'Description'
        '''
        id = re.compile(r'<script type="text/javascript"> id_film = (\d+); </script>').findall(content)
        if id:
            object.id = self.prepare_int(id[0])

        title = re.compile(r'<h1 style="margin: 0; padding: 0" class="moviename-big">(.+?)</h1>').findall(content)
        if title:
            object.title = self.prepare_str(title[0])

        title_original = re.compile(r'<span style="color: #666; font-size: 13px">(.+?)</span>').findall(content)
        if title_original:
            object.title_original = self.prepare_str(title_original[0])

        plot = re.compile(r'<span class="_reachbanner_">(.+?)</span>').findall(content)
        if plot != []:
            object.plot = self.prepare_str(plot[0])

        content_info = content[content.find(u'<!-- инфа о фильме -->'):content.find(u'<!-- /инфа о фильме -->')]
        content_info = re.compile(r'<tr><td class="type">(.+?)</td><td[^>]*>(.+?)</td></tr>').findall(content_info)
        for name, value in content_info:
            if name == u'слоган':
                object.tagline = self.prepare_str(value)
            elif name == u'время':
                object.runtime = self.prepare_str(value)
            elif name == u'год':
                # <a href="/level/10/m_act%5Byear%5D/1960/">1960</a>&nbsp;<a href='/level/44/film/229562/' class='all'>(6 сезонов)</a>
                year = re.compile(r'<a href="/level/10/m_act%5Byear%5D/\d{4}/">(\d{4})</a>').findall(value)
                if year:
                    object.year = self.prepare_int(year[0])

        object.set_source('main_page')

class MoviePostersPage(KinopoiskPage):
    '''
    Class for parsing movie's posters page purpose
    >>> m = Movie(id=51319)
    >>> m.get_content('posters')
    >>> m.posters
    [1207166, 1196342, 1151730, 1151729, 1151728, 1151727, 1151726, 1151725, 1143914, 1139214, 1128415, 1118895, 1114967, 1112313, 1112312, 1112310, 1106582, 1091867, 1074616, 1064821, 973448]
    '''
    url = '/level/17/film/%d/'

    def get(self, object):
        content = UrlRequest(object.get_url('posters')).read()

        # header with sign 'No posters'
        if re.findall(r'<h1 class="main_title">', content):
            return False

        soup_content = BeautifulSoup(content)
        table = soup_content.findAll('table', attrs={'class': re.compile('^fotos')})
        if table:
            self.parse(object, unicode(table[0]))
        else:
            raise ValueError('Parse error. Do not found posters for movie %s' % (object.get_url('posters')))

    def parse(self, object, content):
        '''
        >>> m = Movie()
        >>> m.parse('posters', u'<table class="fotos"><tr><td><a href="/picture/1207166/"><img  src="/images/poster/sm_1207166.jpg" width="170" height="244" alt="Просмотр фото" title="Просмотр постера" /></a><b><i>800&times;1148</i><a href="/picture/1207166/" target="_blank" title="Открыть в новом окне"></a>598 Кб</b></td><td class="center"><a href="/picture/1196342/"><img  src="/images/poster/sm_1196342.jpg" width="170" height="238" alt="Просмотр фото" title="Просмотр постера" /></a><b><i>394&times;552</i><a href="/picture/1196342/" target="_blank" title="Открыть в новом окне"></a>96 Кб</b></td><td><a href="/picture/1151730/"><img  src="/images/poster/sm_1151730.jpg" width="170" height="241" alt="Просмотр фото" title="Просмотр постера" /></a><b><i>400&times;568</i><a href="/picture/1151730/" target="_blank" title="Открыть в новом окне"></a>43 Кб</b></td></tr></table>')
        >>> m.posters
        [1207166, 1196342, 1151730]
        '''
        links = BeautifulSoup(content).findAll('a')
        for link in links:
            id = re.compile(r'/picture/(\d+)/').findall(link['href'])
            try:
                id = int(id[0])
                if id not in object.posters:
                    object.posters += [id]
            except:
                pass

        object.set_source('posters')

class Movie(KinopoiskObject):

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

    posters = []

    def __init__(self, **kwargs):
        super(Movie, self).__init__(**kwargs)
        self.register_source('link', MovieLink)
        self.register_source('main_page', MovieMainPage)
        self.register_source('posters', MoviePostersPage)
        self.posters = self.audience = []

    def __repr__(self):
        return '%s (%s), %s' % (self.title, self.title_original, self.year)

    def get_posters(self):
        title = self.title.replace(' ', '-') if self.title else 'Title'
        return ['http://st3.kinopoisk.ru/im/poster/1/1/1/kinopoisk.ru-%s-%d.jpg' % (title, id) for id in self.posters]

class MovieManager(Manager):
    '''
    >>> movies = Movie.objects.search('Redacted')
    >>> len(movies) == 1
    True
    >>> m = movies[0]
    >>> m.id
    278229
    >>> m.year
    2007
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
    >>> m.id
    342
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