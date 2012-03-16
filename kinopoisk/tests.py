# -*- coding: utf-8 -*-
import unittest
from datetime import datetime
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

    def test_movie_premier_link_source(self):

        m = Movie()
        m.parse('premier_link', u'''<div class="premier_item" id="544226" style="z-index:999;" itemscope="" itemtype="http://schema.org/Event">
   <meta itemprop="startDate" content="2012-03-15">
   <meta itemprop="image" content="http://st.kinopoisk.ru/images/sm_film/544226.jpg">
   <div class="image">
      <a href="/level/1/film/544226/" itemprop="url"><img src="http://st.kinopoisk.ru/images/sm_film/544226.jpg" class="" title="" style="width: 52px; border-top-width: 3px; border-right-width: 3px; border-bottom-width: 3px; border-left-width: 3px; border-top-color: rgb(255, 102, 0); border-right-color: rgb(255, 102, 0); border-bottom-color: rgb(255, 102, 0); border-left-color: rgb(255, 102, 0); border-top-style: solid; border-right-style: solid; border-bottom-style: solid; border-left-style: solid; border-image: initial; display: block; margin-top: 5px; margin-right: 0px; margin-bottom: 5px; margin-left: 0px; opacity: 1; " alt="Белоснежка: Месть гномов" id="FlappImg_1"></a>
   </div>
   <div class="text">
      <div class="textBlock">
         <span class="name_big" itemprop="name"><a href="/level/1/film/544226/">Белоснежка: Месть гномов</a></span>
         <span> Mirror Mirror  (2012)</span>
         <span style="margin: 0">
            США,
            <i>реж. <a class="lined" href="/level/4/people/8764/">Тарсем Синх</a></i>
         </span>
         <span>(фэнтези, драма, комедия...)</span>
         <span><a class="lined" href="/level/4/people/16564/">Джулия Робертс</a>, <a class="lined" href="/level/4/people/1801793/">Лили Коллинз</a></span>
      </div>
      <span class="sinopsys" itemprop="description">Злая Королева, мечтающая выйти замуж за красивого и богатого Принца, хитростью выдворяет из дворца Белоснежку и берет власть в свои руки. Но милая девушка не погибла в темном дремучем лесу, а связалась с бандой гномов-разбойников. Вместе они отомстят Злодейке!</span>
   </div>
   <div class="prem_day">
      <div class="day"><div><img src="http://st.kinopoisk.ru/images/dates/1g.gif" width="28" height="40"><img src="http://st.kinopoisk.ru/images/dates/5g.gif" width="28" height="40"><br><img src="http://st.kinopoisk.ru/images/dates/month_03g.gif" vspace="6"><br></div></div>
          <s class="company"><a href="/level/8/view/prem/company/4/">Парадиз</a></s>
      <div class="limited"></div>
   </div>
   <div class="clear"></div>
   <span id="ur_rating_544226" class="ajax_rating"><i>Рейтинг фильма:<u>6.68 &nbsp; <b>329</b></u></i></span>
   <div class="my_mark" id="my_vote_544226" title="Моя оценка"></div>
   <div class="MyKP_Folder_Select shortselect" id="MyKP_Folder_544226" type="film"><div class="select" id="select_544226"><span class="title" onclick="ClickFolders(this)">Мои фильмы <b></b></span><div class="list_div"></div></div></div>
</div>''')
        self.assertEqual(m.id, 544226)
        self.assertEqual(m.title, u'Белоснежка: Месть гномов')
        self.assertEqual(m.title_original, 'Mirror Mirror')
        self.assertEqual(m.year, 2012)
        self.assertEqual(m.release, datetime(2012,3,15))
        self.assertEqual(m.plot, u'Злая Королева, мечтающая выйти замуж за красивого и богатого Принца, хитростью выдворяет из дворца Белоснежку и берет власть в свои руки. Но милая девушка не погибла в темном дремучем лесу, а связалась с бандой гномов-разбойников. Вместе они отомстят Злодейке!')

        m = Movie()
        m.parse('premier_link', u'''<div class="premier_item" id="2360" style="z-index:992;" itemscope="" itemtype="http://schema.org/Event">
   <meta itemprop="startDate" content="2012-03-22">
   <meta itemprop="image" content="http://st.kinopoisk.ru/images/sm_film/2360.jpg">
   <div class="image gray">
      <a href="/level/1/film/2360/" itemprop="url"><img src="http://st.kinopoisk.ru/images/sm_film/2360.jpg" class="" title="" style="width: 52px; border-top-width: 3px; border-right-width: 3px; border-bottom-width: 3px; border-left-width: 3px; border-top-color: rgb(255, 102, 0); border-right-color: rgb(255, 102, 0); border-bottom-color: rgb(255, 102, 0); border-left-color: rgb(255, 102, 0); border-top-style: solid; border-right-style: solid; border-bottom-style: solid; border-left-style: solid; border-image: initial; display: block; margin-top: 5px; margin-right: 0px; margin-bottom: 5px; margin-left: 0px; opacity: 1; " alt="Король Лев" id="FlappImg_8"></a>
          <b><a href="/level/8/view/prem/only3d/yes/">3D</a></b>
   </div>
   <div class="text">
      <div class="textBlock">
         <span class="name" itemprop="name"><a href="/level/1/film/2360/">Король Лев</a></span>
         <span> The Lion King  (1994)</span>
         <span style="margin: 0">
            США,
            <i>реж. <a class="lined" href="/level/4/people/7313/">Роджер Аллерс</a>...</i>
         </span>
         <span>(мультфильм, мюзикл, драма...)</span>
         <span><a class="lined" href="/level/4/people/33061/">Джереми Айронс</a>, <a class="lined" href="/level/4/people/10968/">Мэттью Бродерик</a></span>
      </div>
   </div>
   <div class="prem_day">
      <div class="day"><div><img src="http://st.kinopoisk.ru/images/dates/2.gif" width="28" height="40"><img src="http://st.kinopoisk.ru/images/dates/2.gif" width="28" height="40"><br><img src="http://st.kinopoisk.ru/images/dates/month_03.gif" vspace="6"><br></div></div>
          <s class="company"><a href="/level/8/view/prem/company/184/">WDSSPR</a></s>
      <div class="limited"></div>
   </div>
   <div class="clear"></div>
   <span id="ur_rating_2360" class="ajax_rating"><i>Рейтинг фильма:<u>8.78 &nbsp; <b>91558</b></u></i></span>
   <div class="my_mark" id="my_vote_2360" title="Моя оценка"></div>
   <div class="MyKP_Folder_Select shortselect" id="MyKP_Folder_2360" type="film"><div class="select" id="select_2360"><span class="title" onclick="ClickFolders(this)">Мои фильмы <b></b></span><div class="list_div"></div></div></div>
</div>''')

        self.assertEqual(m.id, 2360)
        self.assertEqual(m.title, u'Король Лев')
        self.assertEqual(m.title_original, 'The Lion King')
        self.assertEqual(m.year, 1994)
        self.assertEqual(m.release, datetime(2012,3,22))

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