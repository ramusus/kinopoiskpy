# -*- coding: utf-8 -*-
# flake8: noqa: E501
from __future__ import unicode_literals

from kinopoisk.person import Person
from .base import BaseTest


class PersonTest(BaseTest):
    def test_person_manager_with_one_result(self):
        persons = Person.objects.search('Гуальтиеро Якопетти')
        self.assertEqual(len(persons), 1)

        m = persons[0]
        self.assertEqual(m.id, 351549)
        self.assertEqual(m.name, 'Гуалтьеро Якопетти')
        self.assertEqual(m.year_birth, 1919)
        self.assertEqual(m.name_en, 'Gualtiero Jacopetti')

    def test_person_manager_with_many_results(self):
        persons = Person.objects.search('malkovich')
        self.assertGreater(len(persons), 1)

        m = persons[0]
        self.assertEqual(m.id, 24508)
        self.assertEqual(m.name, 'Джон Малкович')
        self.assertEqual(m.year_birth, 1953)
        self.assertEqual(m.name_en, 'John Malkovich')

    def test_person_main_page_source(self):
        m = Person(id=6245)
        m.get_content('main_page')
        self.assertEqual(m.id, 6245)
        self.assertEqual(m.name, 'Джонни Депп')
        self.assertEqual(m.year_birth, 1963)
        self.assertEqual(m.name_en, 'Johnny Depp')
        self.assertGreater(len(m.information), 50)

    def test_person_photos_page_source(self):
        m = Person(id=8217)
        m.get_content('photos')
        self.assertGreaterEqual(len(m.photos), 11)

    def test_person_repr(self):
        instance = Person(name='Чарльз Чаплин', name_en='Charles Chaplin', year_birth='1950')
        self.assertEqual(instance.__repr__(), 'Чарльз Чаплин (Charles Chaplin), 1950')
