# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from future.utils import python_2_unicode_compatible

from .sources import PersonLink, PersonMainPage, PersonPhotosPage
from ..utils import KinopoiskObject, Manager


@python_2_unicode_compatible
class Person(KinopoiskObject):
    """
    Person Class
    """
    def set_defaults(self):
        self.name = ''
        self.name_original = ''
        self.information = ''

        self.year_birth = None

        self.photos = []

    def __init__(self, *args, **kwargs):
        super(Person, self).__init__(*args, **kwargs)

        self.register_source('link', PersonLink)
        self.register_source('main_page', PersonMainPage)
        self.register_source('photos', PersonPhotosPage)

        self.set_url('info', '/handler_info.php?token={token}&obj_type={type}&obj_id={id}')

    def __repr__(self):
        return '{} ({}), {}'.format(self.name, self.name_original, self.year_birth or '-')


class PersonManager(Manager):
    """
    Person manager
    """
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
