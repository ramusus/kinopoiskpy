# -*- coding: utf-8 -*-
import unittest
from kinopoisk import Movie, Person

class MovieTest(unittest.TestCase):

    def test_movie_link_source(self):
        '''
        Test of parsing movie link in search results
        '''
        m = Movie()
        m.parse('link', u'''<p class="pic"><a href="/level/1/film/342/sr/1/"><img class="flap_img" src="http://st.kinopoisk.ru/images/spacer.gif" title="/images/sm_film/342.jpg" alt="Криминальное чтиво" title="Криминальное чтиво" /></a></p>
            <div class="info">
            <p class="name"><a href="/level/1/film/342/sr/1/">Криминальное чтиво</a> <span class="year">1994</span></p>
            <span class="gray">Pulp Fiction, 154 мин</span>
            <span class="gray">США, <i class="director">реж. <a class="lined" href="/level/4/people/7640/">Квентин Тарантино</a></i>
            <br />(триллер, криминал)
                 </span>
            <span class="gray">
            <a class="lined" href="/level/4/people/6479/">Джон Траволта</a>, <a class="lined" href="/level/4/people/7164/">Сэмюэл Л. Джексон</a>, <a class="lined" href="/level/19/film/342/#actor">...</a>
            </span>
            </div>
            <div class="clear"></div>
            </div>''')
        self.assertEqual(m.title, u'Криминальное чтиво')
        self.assertEqual(m.id, 342)
        self.assertEqual(m.runtime, 154)
        self.assertEqual(m.year, 1994)
        self.assertEqual(m.title_original, u'Pulp Fiction')

        m = Movie()
        m.parse('link', u'<div class="element width_2"><span class="gray"></span></div>')
        self.assertEqual(m.runtime, None)
        self.assertEqual(m.title_original, '')

        m = Movie()
        m.parse('link', u'<div class="element width_2"><span class="gray">Zdar Buh, hosi!</span></div>')
        self.assertEqual(m.runtime, None)
        self.assertEqual(m.title_original, u'Zdar Buh, hosi!')

    def test_movie_main_page_source(self):
        '''
        Test of parsing movie info from movie page
        '''
        m = Movie()
        m.parse('main_page', u'<h1 style="margin: 0; padding: 0" class="moviename-big">Title</h1><div class="brand_words" itemprop="description">Description</div>')
        self.assertEqual(m.title, u'Title')
        self.assertEqual(m.plot, u'Description')

    def test_movie_posters_page_source(self):
        '''
        Test of parsing movie posters
        '''
        m = Movie()
        m.parse('posters', u'<table class="fotos"><tr><td><a href="/picture/1207166/"><img  src="/images/poster/sm_1207166.jpg" width="170" height="244" alt="Просмотр фото" title="Просмотр постера" /></a><b><i>800&times;1148</i><a href="/picture/1207166/" target="_blank" title="Открыть в новом окне"></a>598 Кб</b></td><td class="center"><a href="/picture/1196342/"><img  src="/images/poster/sm_1196342.jpg" width="170" height="238" alt="Просмотр фото" title="Просмотр постера" /></a><b><i>394&times;552</i><a href="/picture/1196342/" target="_blank" title="Открыть в новом окне"></a>96 Кб</b></td><td><a href="/picture/1151730/"><img  src="/images/poster/sm_1151730.jpg" width="170" height="241" alt="Просмотр фото" title="Просмотр постера" /></a><b><i>400&times;568</i><a href="/picture/1151730/" target="_blank" title="Открыть в новом окне"></a>43 Кб</b></td></tr></table>')
        self.assertEqual(m.posters, [1207166, 1196342, 1151730])

        m = Movie(id=51319)
        m.get_content('posters')
        self.assertEqual(m.posters, [1207166, 1196342, 1151730, 1151729, 1151728, 1151727, 1151726, 1151725, 1143914, 1139214, 1128415, 1118895, 1114967, 1112313, 1112312, 1112310, 1106582, 1091867, 1074616, 1064821, 973448])

    def test_movie(self):
        '''
        Test of movie manager
        '''
        movies = Movie.objects.search('Redacted')
        self.assertTrue(len(movies) == 1)

        m = movies[0]
        self.assertEqual(m.id, 278229)
        self.assertEqual(m.year, 2007)
        self.assertEqual(m.title, u'Без цензуры')
        self.assertEqual(m.title_original, u'Redacted')
        self.assertEqual(m.plot, u'В центре картины  -  небольшой отряд американских солдат на контрольно-пропускном пункте в Ираке. Причём восприятие их истории постоянно меняется. Мы видим события глазами самих солдат, представителей СМИ, иракцев и понимаем, как на каждого из них влияет происходящее, их встречи и столкновения друг с другом.')
        self.assertEqual(m.runtime, 90)
        self.assertEqual(m.tagline, u'"Фильм, запрещенный к прокату во многих странах"')

        movies = Movie.objects.search('pulp fiction')
        self.assertTrue(len(movies) > 1)

        m = movies[0]
        self.assertEqual(m.id, 342)
        self.assertEqual(m.title, u'Криминальное чтиво')
        self.assertEqual(m.year, 1994)
        self.assertEqual(m.title_original, u'Pulp Fiction')

class PersonTest(unittest.TestCase):

    def test_person(self):
        '''
        Test of person manager
        '''
        persons = Person.objects.search(u'Гуальтиеро Якопетти')
        self.assertTrue(len(persons) == 1)

        m = persons[0]
        self.assertEqual(m.id, 351549)
        self.assertEqual(m.name, u'Гуалтьеро Якопетти')
        self.assertEqual(m.year_birth, 1919)
        self.assertEqual(m.name_original, u'Gualtiero Jacopetti')

        persons = Person.objects.search('malkovich')
        self.assertTrue(len(persons) > 1)

        m = persons[0]
        self.assertEqual(m.id, 24508)
        self.assertEqual(m.name, u'Джон Малкович')
        self.assertEqual(m.year_birth, 1953)
        self.assertEqual(m.name_original, u'John Malkovich')

    def test_person_link_source(self):
        '''
        Test of parsing person link in search results
        '''
        m = Person()
        m.parse('link', u'<div class="element most_wanted"> \
            <p class="pic"><a href="http://www.kinopoisk.ru/level/4/people/24508/sr/1/"><img src="/images/sm_actor/24508.jpg" alt="Name" title="Name" /></a></p> \
            <div class="info"> \
            <p class="name"><a href="http://www.kinopoisk.ru/level/4/people/24508/sr/1/">Name</a>, <span class="year">1953</span></p> \
            <span class="gray">John Malkovich</span> \
            <span class="gray"> \
            </span> \
            </div> \
            </div>')
        self.assertEqual(m.name, u'Name')
        self.assertEqual(m.id, 24508)
        self.assertEqual(m.year_birth, 1953)
        self.assertEqual(m.name_original, u'John Malkovich')

if __name__ == '__main__':
    unittest.main()