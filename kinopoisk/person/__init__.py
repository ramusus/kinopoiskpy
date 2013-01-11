# -*- coding: utf-8 -*-
from kinopoisk.utils import KinopoiskObject, Manager

class Person(KinopoiskObject):

    name = ''
    name_original = ''
    information = ''

    year_birth = None

    photos = []

    def __init__(self, **kwargs):
        super(Person, self).__init__(**kwargs)
        from sources import PersonLink, PersonMainPage, PersonPhotosPage # import here for successful installing via pip
        self.register_source('link', PersonLink)
        self.register_source('main_page', PersonMainPage)
        self.register_source('photos', PersonPhotosPage)
        self.posters = self.audience = []

        self.set_url('info', '/handler_info.php?obj_type=actor&obj_id=%d')

    def __repr__(self):
        return ('<%s (%s), %s>' % (self.name, self.name_original, self.year_birth or '-')).encode('utf-8')

    def get_photos(self):
        return self.photos

class PersonManager(Manager):
    '''
    Person manager
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
