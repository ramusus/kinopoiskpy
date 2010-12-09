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
        >>> m.parse('link', u'<div class="element most_wanted"> \
            <p class="pic"><a href="/level/4/people/24508/sr/1/"><img src="/images/sm_actor/24508.jpg" alt="Name" title="Name" /></a></p> \
            <div class="info"> \
            <p class="name"><a href="/level/4/people/24508/sr/1/">Name</a>, <span class="year"><a href="/level/10/act/birthday/view/year/year/1953/">1953</a></span></p> \
            <span class="gray">John Malkovich</span> \
            <span class="gray"> \
            </span> \
            </div> \
            </div>')
        >>> m.name
        u'Name'
        >>> m.id
        24508
        >>> m.year_birth
        1953
        >>> m.name_original
        u'John Malkovich'
        '''
        link = re.compile(r'<p class="name"><a href="/level/4/people/(\d+)/[^"]*">(.+?)</a>').findall(content)
        if link:
            object.id = self.prepare_int(link[0][0])
            object.name = self.prepare_str(link[0][1])

        year = re.compile(r'<a href="/level/10/act/birthday/view/year/year/(\d{4})/"').findall(content)
        if year:
            object.year_birth = self.prepare_int(year[0])

        otitle = re.compile(r'<span class="gray">(.*?)</span>').findall(content)
        if otitle:
            object.name_original = self.prepare_str(otitle[0])

        object.set_source('link')

class PersonMainPage(KinopoiskPage):
    '''
    Class for parsing main person page purpose
    '''
    url = '/level/4/people/%d/'

    def parse(self, object, content):

        id = re.compile(r"<script>stars\('id_actor','(\d+)'\);</script>").findall(content)
        if id:
            object.id = self.prepare_int(id[0])

        name = re.compile(r'<h1 style="padding:0px;margin:0px" class="moviename-big">(.+?)</h1>').findall(content)
        if name:
            object.name = self.prepare_str(name[0])

        name_original = re.compile(r'<span style="font-size:13px;color:#666">(.+?)</span>').findall(content)
        if name_original:
            object.name_original = self.prepare_str(name_original[0])

        content_info = content[content.find(u'<!-- инфа об актере -->'):content.find(u'<!-- /инфа об актере -->')]
        content_info = re.compile(r'<tr><td class="type">(.+?)</td><td[^>]*>(.+?)</td></tr>').findall(content_info)
        for name, value in content_info:
            if name == u'дата рождения':
                year_birth = re.compile(r'<a href="/level/10/m_act\[birthday\]\[year\]/\d{4}/">(\d{4})</a>').findall(value)
                if year_birth:
                    object.year_birth = self.prepare_int(year_birth[0])

        object.set_source('main_page')

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
    >>> persons = Person.objects.search(u'\u0413\u0443\u0430\u043b\u044c\u0442\u0438\u0435\u0440\u043e \u042f\u043a\u043e\u043f\u0435\u0442\u0442\u0438')
    >>> len(persons) == 1
    True
    >>> m = persons[0]
    >>> m.id
    351549
    >>> m.name
    u'\u0414\u0436\u0443\u0430\u043b\u044c\u0442\u0435\u0440\u043e \u042f\u043a\u043e\u043f\u0435\u0442\u0442\u0438'
    >>> m.year_birth
    1919
    >>> m.name_original
    u'Gualtiero Jacopetti'

#    >>> persons = Person.objects.search('malkovich')
#    >>> len(persons) > 1
#    True
#    >>> m = persons[0]
#    >>> m.id
#    24508
#    >>> m.name
#    u'\u0414\u0436\u043e\u043d \u041c\u0430\u043b\u043a\u043e\u0432\u0438\u0447'
#    >>> m.year_birth
#    1953
#    >>> m.name_original
#    u'John Malkovich'
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