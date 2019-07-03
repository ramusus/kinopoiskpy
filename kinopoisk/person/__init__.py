# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from future.utils import python_2_unicode_compatible

from .sources import PersonLink, PersonShortLink, PersonMainPage, PersonPhotosPage, PersonRoleLink, PersonCastLink
from ..utils import KinopoiskObject, Manager


@python_2_unicode_compatible
class Person(KinopoiskObject):
    """
    Person Class
    """
    def set_defaults(self):
        self.name = ''
        self.name_en = ''
        self.information = ''

        self.year_birth = None

        self.career = {}
        self.photos = []

    def __init__(self, *args, **kwargs):
        super(Person, self).__init__(*args, **kwargs)

        self.register_source('link', PersonLink)
        self.register_source('cast_link', PersonCastLink)
        self.register_source('short_link', PersonShortLink)
        self.register_source('main_page', PersonMainPage)
        self.register_source('photos', PersonPhotosPage)

        self.set_url('info', '/handler_get_trivia_list.php?token={token}&obj_type={type}&obj_id={id}')

    def __repr__(self):
        repr = self.name
        if self.name_en:
            repr += ' ({})'.format(self.name_en)
        if self.year_birth:
            repr += ', {}'.format(self.year_birth)
        return repr


@python_2_unicode_compatible
class Role(KinopoiskObject):
    """
    Person Role Class
    """
    def set_defaults(self):
        self.name = ''
        self.movie = None
        self.voice = False

    def __init__(self, *args, **kwargs):
        super(Role, self).__init__(*args, **kwargs)

        self.register_source('role_link', PersonRoleLink)


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
