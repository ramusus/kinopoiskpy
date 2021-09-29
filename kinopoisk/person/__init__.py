# -*- coding: utf-8 -*-
from .sources import PersonLink, PersonShortLink, PersonMainPage, PersonPhotosPage, PersonRoleLink, PersonCastLink
from ..utils import KinopoiskObject, Manager


class Person(KinopoiskObject):
    """
    Person Classtest_person_cast_special_case
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


Person.objects = PersonManager()
