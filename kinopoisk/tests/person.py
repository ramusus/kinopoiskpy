# -*- coding: utf-8 -*-
# flake8: noqa: E501
from __future__ import unicode_literals

from kinopoisk.person import Person
from .base import BaseTest


class PersonTest(BaseTest):
    def test_person_manager_with_one_result(self):
        persons = Person.objects.search('Гуальтиеро Якопетти')
        self.assertEqual(len(persons), 1)

        p = persons[0]
        self.assertEqual(p.id, 351549)
        self.assertEqual(p.name, 'Гуалтьеро Якопетти')
        self.assertEqual(p.year_birth, 1919)
        self.assertEqual(p.name_en, 'Gualtiero Jacopetti')

    def test_person_manager_with_many_results(self):
        persons = Person.objects.search('malkovich')
        self.assertGreater(len(persons), 1)

        p = persons[0]
        self.assertEqual(p.id, 24508)
        self.assertEqual(p.name, 'Джон Малкович')
        self.assertEqual(p.year_birth, 1953)
        self.assertEqual(p.name_en, 'John Malkovich')

        p = persons[4]
        self.assertEqual(p.name, 'Др. Марк Малкович III')
        self.assertEqual(p.year_birth, 1930)
        self.assertEqual(p.year_death, 2010)

    def test_person_main_page_source(self):
        p = Person(id=6245)
        p.get_content('main_page')
        self.assertEqual(p.id, 6245)
        self.assertEqual(p.name, 'Джонни Депп')
        self.assertEqual(p.year_birth, 1963)
        self.assertEqual(p.name_en, 'Johnny Depp')
        self.assertGreater(len(p.information), 50)

        # career
        self.assertGreaterEqual(len(p.career['actor']), 86)
        self.assertGreaterEqual(len(p.career['producer']), 7)
        self.assertGreaterEqual(len(p.career['director']), 3)
        self.assertGreaterEqual(len(p.career['writer']), 1)
        self.assertGreaterEqual(len(p.career['hrono_titr_male']), 11)
        self.assertGreaterEqual(len(p.career['himself']), 124)

        self.assertEqual(p.career['actor'][0].movie.id, 420454)
        self.assertEqual(p.career['actor'][0].movie.title, 'Человек-невидимка')
        self.assertEqual(p.career['actor'][0].movie.title_en, 'The Invisible Man')
        self.assertEqual(p.career['actor'][0].name, 'Dr. Griffin')

        self.assertEqual(p.career['actor'][1].movie.title, 'Ричард прощается')
        self.assertEqual(p.career['actor'][1].movie.year, 2018)
        self.assertEqual(p.career['actor'][1].movie.title_en, 'Richard Says Goodbye')

        self.assertEqual(p.career['actor'][4].movie.title, 'Шерлок Гномс')
        self.assertEqual(p.career['actor'][4].movie.title_en, 'Sherlock Gnomes')
        self.assertEqual(p.career['actor'][4].movie.year, 2018)
        self.assertEqual(p.career['actor'][4].name, 'Sherlock Gnomes')  # voice

        self.assertEqual(p.career['actor'][5].movie.title_en, 'Murder on the Orient Express')
        self.assertAlmostEqual(p.career['actor'][5].movie.rating, 6.68)
        self.assertGreaterEqual(p.career['actor'][5].movie.votes, 64162)
        self.assertAlmostEqual(p.career['actor'][5].movie.imdb_rating, 6.6)
        self.assertGreaterEqual(p.career['actor'][5].movie.imdb_votes, 70581)

        self.assertEqual(p.career['actor'][6].name, 'Abel')  # short

        # series
        self.assertEqual(p.career['actor'][22].name, 'Johnny Depp')
        self.assertEqual(p.career['actor'][22].movie.title, 'Жизнь так коротка')
        self.assertEqual(p.career['actor'][22].movie.title_en, 'Life\'s Too Short')
        self.assertEqual(p.career['actor'][22].movie.year, None)
        self.assertEqual(p.career['actor'][22].movie.series, True)
        self.assertEqual(p.career['actor'][22].movie.series_years, (2011, 2013))

        # top + budget
        self.assertEqual(p.career['actor'][34].name, 'Jack Sparrow')
        self.assertEqual(p.career['actor'][34].movie.title, 'Пираты Карибского моря: Сундук мертвеца')
        self.assertEqual(p.career['actor'][34].movie.title_en, 'Pirates of the Caribbean: Dead Man\'s Chest')
        self.assertEqual(p.career['actor'][34].movie.year, 2006)

        # voice and short
        self.assertEqual(p.career['actor'][35].name, 'Narration')
        self.assertEqual(p.career['actor'][35].movie.genres, ['короткометражка'])
        self.assertEqual(p.career['actor'][35].voice, True)

        # endless series
        self.assertEqual(p.career['actor'][55].name, 'Jack Kahuna Laguna')
        self.assertEqual(p.career['actor'][55].movie.title, 'Губка Боб квадратные штаны')
        self.assertEqual(p.career['actor'][55].movie.title_en, 'SpongeBob SquarePants')
        self.assertEqual(p.career['actor'][55].movie.year, None)
        self.assertEqual(p.career['actor'][55].movie.series, True)
        self.assertEqual(p.career['actor'][55].movie.series_years, (1999,))

        # short, no russian title
        self.assertEqual(p.career['actor'][82].name, 'Pete')
        self.assertEqual(p.career['actor'][82].movie.title, '')
        self.assertEqual(p.career['actor'][82].movie.title_en, 'Dummies')
        self.assertEqual(p.career['actor'][82].movie.year, 1985)
        self.assertEqual(p.career['actor'][82].movie.genres, ['короткометражка'])
        self.assertEqual(p.career['actor'][82].movie.rating, None)
        self.assertEqual(p.career['actor'][82].movie.votes, None)

    def test_person_cast_special_case(self):
        p = Person(id=9843)
        p.get_content('main_page')

        # ... in movie title
        self.assertEqual(p.career['actor'][137].name, None)
        self.assertEqual(p.career['actor'][137].movie.title, 'Тарзан и Джейн возвращены... как будто')
        self.assertEqual(p.career['actor'][137].movie.title_en, 'Tarzan and Jane Regained... Sort of')
        self.assertEqual(p.career['actor'][137].movie.year, 1964)

    def test_person_photos_page_source(self):
        p = Person(id=8217)
        p.get_content('photos')
        self.assertGreaterEqual(len(p.photos), 11)

    def test_person_repr(self):
        instance = Person(name='Чарльз Чаплин', name_en='Charles Chaplin', year_birth='1950')
        self.assertEqual(instance.__repr__(), 'Чарльз Чаплин (Charles Chaplin), 1950')
