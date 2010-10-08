# -*- coding: utf-8 -*-
from utils import KinopoiskObject, KinopoiskPage, Manager
import re
import sys

class PersonLink(KinopoiskPage):
    '''
    Class for parsing person info from links
    '''
    def parse(self, object, content):
        '''
        >>> m = Person()
        >>> m.parse('link', u'<td width=100% class="news"><a class="all" href="/level/4/people/24508/sr/1/">Name</a>,&nbsp;<a href="/level/10/act/birthday/view/year/year/1953/" class=orange>1953</a></td> </tr><tr><td></td><td><i class="search_rating"></i><font color="#999999">... John Malkovich</font></td> </tr>')
        >>> m.name
        u'Name'
        >>> m.id
        24508
        >>> m.year_birth
        1953
        >>> m.name_original
        u'John Malkovich'
        '''
        link = re.compile(r'<a class="all" href="/level/4/people/(\d+)/[^"]*">(.+?)</a>').findall(content)
        if link:
            object.id = self.prepare_int(link[0][0])
            object.name = self.prepare_str(link[0][1])

        year = re.compile(r'<a href="/level/10/act/birthday/view/year/year/(\d{4})/"').findall(content)
        if year:
            object.year_birth = self.prepare_int(year[0])

        otitle = re.compile(r'<font color="#999999">(.+?)</font>').findall(content)
        if otitle:
            object.name_original = self.prepare_str(re.sub(r'^\.\.\. ', '', otitle[0]))

        object.set_source('link')

class PersonMainPage(KinopoiskPage):
    '''
    Class for parsing main person page purpose
    '''
    url = '/level/4/people/%d/'

    def parse(self, object, content):
#        '''
#        >>> m = Person()
#        >>> m.parse_main_page(u'<h1 style="margin: 0; padding: 0" class="moviename-big">Title</h1><span class="_reachbanner_">Description</span>')
#        >>> m.title
#        u'Title'
#        >>> m.plot
#        u'Description'
#        '''
#        title = re.compile(r'<h1 style="margin: 0; padding: 0" class="moviename-big">(.+?)</h1>').findall(content)
#        if title:
#            self.title = self.prepare_str(title[0])
#
#        title_original = re.compile(r'<span style="color: #666; font-size: 13px">(.+?)</span>').findall(content)
#        if title_original:
#            self.title_original = self.prepare_str(title_original[0])
#
#        plot = re.compile(r'<span class="_reachbanner_">(.+?)</span>').findall(content)
#        if plot != []:
#            self.plot = self.prepare_str(plot[0])
#
#        content_info = content[content.find(u'<!-- инфа о фильме -->'):content.find(u'<!-- /инфа о фильме -->')]
#        content_info = re.compile(r'<tr><td class="type">(.+?)</td><td[^>]*>(.+?)</td></tr>').findall(content_info)
#        for name, value in content_info:
#            if name == u'слоган':
#                self.tagline = self.prepare_str(value)
#            elif name == u'время':
#                self.runtime = self.prepare_str(value)

        self.set_source('main_page')

class Person(KinopoiskObject):

    name = None
    name_original = None

    year_birth = None

    def __init__(self, **kwargs):
        super(Person, self).__init__(**kwargs)
        self.register_source('link', PersonLink)
        self.register_source('main_page', PersonMainPage)
        self.posters = self.audience = []

    def __repr__(self):
        return '%s (%s), %s' % (self.name, self.name_original, self.year_birth)

class PersonManager(Manager):
    '''
    >>> persons = Person.objects.search('malkovich')
    >>> len(persons) > 1
    True
    >>> m = persons[0]
    >>> m.name
    u'\u0414\u0436\u043e\u043d \u041c\u0430\u043b\u043a\u043e\u0432\u0438\u0447'
    >>> m.year_birth
    1953
    >>> m.name_original
    u'John Malkovich'
    '''
    kinopoisk_object = Person

    def get_url_with_params(self, query):
        # http://www.kinopoisk.ru/index.php?level=7&from=forma&result=adv&m_act[from]=forma&m_act[what]=content&m_act[find]=pulp+fiction
        # http://www.kinopoisk.ru/index.php?level=7&from=forma&result=adv&m_act[from]=forma&m_act[what]=actor&m_act[find]=malkovich
        return ('http://www.kinopoisk.ru/index.php', {
            'level': 7,
            'from': 'forma',
            'result': 'adv',
            'm_act[from]': 'forma',
            'm_act[what]': 'actor',
            'm_act[find]': query,
        })

Person.objects = PersonManager()

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)