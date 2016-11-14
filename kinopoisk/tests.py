# -*- coding: utf-8 -*-
# flake8: noqa: E501
from __future__ import unicode_literals
import unittest

from datetime import datetime
from .movie import Movie
from .person import Person


class MovieTest(unittest.TestCase):

    def test_movie_link_source(self):
        """
        Test of parsing movie link in search results
        """
        m = Movie()
        m.parse('link', """<p class="pic"><a href="/level/1/film/342/sr/1/"><img class="flap_img" src="http://st.kinopoisk.ru/images/spacer.gif" title="/images/sm_film/342.jpg" alt="Криминальное чтиво" title="Криминальное чтиво" /></a></p>
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
            </div>""")
        self.assertEqual(m.title, 'Криминальное чтиво')
        self.assertEqual(m.id, 342)
        self.assertEqual(m.runtime, 154)
        self.assertEqual(m.year, 1994)
        self.assertEqual(m.title_original, 'Pulp Fiction')

        m = Movie()
        m.parse('link', '<div class="element width_2"><span class="gray"></span></div>')
        self.assertEqual(m.runtime, None)
        self.assertEqual(m.title_original, '')

        m = Movie()
        m.parse('link', '<div class="element width_2"><span class="gray">Zdar Buh, hosi!</span></div>')
        self.assertEqual(m.runtime, None)
        self.assertEqual(m.title_original, 'Zdar Buh, hosi!')

    def test_movie_main_page_source(self):
        """
        Test of parsing movie info from movie page
        """
        m = Movie()
        m.parse('main_page', '<h1 style="margin: 0; padding: 0" class="moviename-big">Title</h1><div class="brand_words" itemprop="description">Description</div>')
        self.assertEqual(m.title, 'Title')
        self.assertEqual(m.plot, 'Description')

    def test_movie_posters_page_source(self):
        """
        Test of parsing movie posters
        """
        m = Movie()
        m.parse('posters', '<table class="fotos"><tr><td><a href="/picture/1207166/"><img  src="/images/poster/sm_1207166.jpg" width="170" height="244" alt="Просмотр фото" title="Просмотр постера" /></a><b><i>800&times;1148</i><a href="/picture/1207166/" target="_blank" title="Открыть в новом окне"></a>598 Кб</b></td><td class="center"><a href="/picture/1196342/"><img  src="/images/poster/sm_1196342.jpg" width="170" height="238" alt="Просмотр фото" title="Просмотр постера" /></a><b><i>394&times;552</i><a href="/picture/1196342/" target="_blank" title="Открыть в новом окне"></a>96 Кб</b></td></tr></table>')
        self.assertEqual(len(m.posters), 2)

        m = Movie(id=51319)
        m.get_content('posters')
        self.assertGreater(len(m.posters), 5)

    def test_movie_premier_link_source(self):

        m = Movie()
        m.parse('premier_link', """<div class="premier_item" id="544226" style="z-index:999;" itemscope="" itemtype="http://schema.org/Event">
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
</div>""")
        self.assertEqual(m.id, 544226)
        self.assertEqual(m.title, 'Белоснежка: Месть гномов')
        self.assertEqual(m.title_original, 'Mirror Mirror')
        self.assertEqual(m.year, 2012)
        self.assertEqual(m.release, datetime(2012, 3, 15))
        self.assertEqual(m.plot, 'Злая Королева, мечтающая выйти замуж за красивого и богатого Принца, хитростью выдворяет из дворца Белоснежку и берет власть в свои руки. Но милая девушка не погибла в темном дремучем лесу, а связалась с бандой гномов-разбойников. Вместе они отомстят Злодейке!')

        m = Movie()
        m.parse('premier_link', """<div class="premier_item" id="2360" style="z-index:992;" itemscope="" itemtype="http://schema.org/Event">
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
</div>""")

        self.assertEqual(m.id, 2360)
        self.assertEqual(m.title, 'Король Лев')
        self.assertEqual(m.title_original, 'The Lion King')
        self.assertEqual(m.year, 1994)
        self.assertEqual(m.release, datetime(2012, 3, 22))

    def test_movie(self):
        """
        Test of movie manager
        """
        movies = Movie.objects.search('Без цензуры 2007')
        self.assertGreater(len(movies), 1)

        m = movies[0]
        self.assertEqual(m.id, 278229)
        self.assertEqual(m.year, 2007)
        self.assertEqual(m.title, 'Без цензуры')
        self.assertEqual(m.title_original, 'Redacted')
        # self.assertEqual(m.plot, 'В центре картины  -  небольшой отряд американских солдат на контрольно-пропускном пункте в Ираке. Причём восприятие их истории постоянно меняется. Мы видим события глазами самих солдат, представителей СМИ, иракцев и понимаем, как на каждого из них влияет происходящее, их встречи и столкновения друг с другом.')
        self.assertEqual(m.runtime, 90)
        # self.assertEqual(m.tagline, '"Фильм, запрещенный к прокату во многих странах"')

        # self.assertEqual(len(m.trailers), 1)
        # self.assertEqual(m.trailers[0].id, 't12964')
        # self.assertEqual(m.trailers[0].file, '278229/kinopoisk.ru-Redacted-22111.flv')
        # self.assertEqual(m.trailers[0].preview_file, '278229/3_6166.jpg')
        # self.assertEqual(m.trailers[0].dom, 'tr')

        movies = Movie.objects.search('pulp fiction')
        self.assertGreater(len(movies), 1)

        m = movies[0]
        self.assertEqual(m.id, 342)
        self.assertEqual(m.title, 'Криминальное чтиво')
        self.assertEqual(m.year, 1994)
        self.assertEqual(m.title_original, 'Pulp Fiction')

    def test_movie_by_id_278229(self):
        """
        Test of movie manager, movie obtain by id (not via search)
        """
        m = Movie(id=278229)
        m.get_content("main_page")
        m.get_content("trailers")

        self.assertEqual(m.id, 278229)
        self.assertEqual(m.year, 2007)
        self.assertEqual(m.title, 'Без цензуры')
        self.assertEqual(m.title_original, 'Redacted')
        self.assertEqual(m.plot, 'В центре картины — небольшой отряд американских солдат на контрольно-пропускном пункте в Ираке. Причём восприятие их истории постоянно меняется. Мы видим события глазами самих солдат, представителей СМИ, иракцев и понимаем, как на каждого из них влияет происходящее, их встречи и столкновения друг с другом.')
        self.assertEqual(m.runtime, 90)
        self.assertEqual(m.tagline, '«Фильм, запрещенный к прокату во многих странах»')
        self.assertEqual(len(m.trailers), 4)
        self.assertEqual(m.trailers[0].id, 't170078')
        self.assertEqual(m.trailers[0].file, '278229/kinopoisk.ru-Redacted-170078.mp4')
        self.assertEqual(m.trailers[0].preview_file, '278229/3_6166.jpg')
        self.assertEqual(m.trailers[0].dom, 'tr')
        self.assertEqual(m.actors, ['Иззи Диаз', 'Роб Дивейни', 'Ти Джонс', 'Анас Веллман', 'Майк Фигуроа',
                                    'Яналь Кассай', 'Дхиая Калиль', 'Кел О’Нил', 'Дэниэл Стюарт-Шерман',
                                    'Патрик Кэрролл'])

        m = Movie(id=746251)
        m.get_content("main_page")
        self.assertEqual(m.year, None)
        self.assertEqual(m.title, 'Ловкость')

        self.assertEqual(m.genres, ['драма'])
        self.assertEqual(m.countries, ['США'])

        # movie with empty actors
        m = Movie(id=926005)
        m.get_content('main_page')
        self.assertEqual(m.actors, [])

    def test_movie_by_id_4374(self):
        """
        Test of movie manager, movie obtain by id (not via search)
        """
        m = Movie(id=4374)
        m.get_content("main_page")
        m.get_content("trailers")

        self.assertEqual(m.id, 4374)
        self.assertEqual(m.year, 2003)
        self.assertEqual(m.title, 'Пираты Карибского моря: Проклятие Черной жемчужины')
        self.assertEqual(m.title_original, 'Pirates of the Caribbean: The Curse of the Black Pearl')
        self.assertEqual(m.plot, 'Жизнь харизматичного авантюриста, капитана Джека Воробья, полная увлекательных приключений, резко меняется, когда его заклятый враг — капитан Барбосса — похищает корабль Джека, Черную Жемчужину, а затем нападает на Порт Ройал и крадет прекрасную дочь губернатора, Элизабет Свонн.Друг детства Элизабет, Уилл Тернер, вместе с Джеком возглавляет спасательную экспедицию на самом быстром корабле Британии, в попытке вызволить девушку из плена и заодно отобрать у злодея Черную Жемчужину. Вслед за этой парочкой отправляется амбициозный коммодор Норрингтон, который к тому же числится женихом Элизабет.Однако Уилл не знает, что над Барбоссой висит вечное проклятие, при лунном свете превращающее его с командой в живых скелетов. Проклятье будет снято лишь тогда, когда украденное золото Ацтеков будет возвращено пиратами на старое место.')
        self.assertEqual(m.runtime, 143)
        self.assertEqual(m.tagline, "«Over 3000 Islands of Paradise -- For Some it's A Blessing -- For Others... It's A Curse»")
        self.assertGreater(len(m.trailers), 2)
        self.assertGreater(len(m.trailers[0].id), 0)
        self.assertGreater(len(m.trailers[0].file), 0)
        self.assertGreater(len(m.trailers[0].preview_file), 0)
        self.assertGreater(len(m.trailers[0].dom), 0)

        self.assertEqual(m.genres, ['фэнтези', 'боевик', 'приключения'])
        self.assertEqual(m.countries, ['США'])
        self.assertGreaterEqual(m.profit_usa, 305413918)
        self.assertGreaterEqual(m.profit_russia, 9060000)
        self.assertGreaterEqual(m.profit_world, 654264015)

        # TODO: still not implemented
        # self.assertEqual(m.directors, ['Гор Вербински'])
        # self.assertEqual(m.scenarios, ['Тед Эллиот', 'Терри Россио', 'Стюарт Битти'])
        # self.assertEqual(m.producers, ['Джерри Брукхаймер', 'Пол Дисон', 'Брюс Хендрикс'])
        # self.assertEqual(m.operators, ['Дариуш Вольски'])
        # self.assertEqual(m.composers, ['Клаус Баделт'])

    def test_movie_by_id_258687(self):
        """
        Test of movie manager, movie obtain by id (not via search)
        """
        m = Movie(id=258687)
        m.get_content("main_page")
        m.get_content("trailers")

        self.assertEqual(m.id, 258687)
        self.assertEqual(m.year, 2014)
        self.assertEqual(m.title, 'Интерстеллар')
        self.assertEqual(m.title_original, 'Interstellar')
        self.assertEqual(m.plot, 'Когда засуха приводит человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину (которая предположительно соединяет области пространства-времени через большое расстояние) в путешествие, чтобы превзойти прежние ограничения для космических путешествий человека и переселить человечество на другую планету.')
        self.assertEqual(m.runtime, 169)
        self.assertEqual(m.tagline, "«Следующий шаг человечества станет величайшим»")
        self.assertGreater(len(m.trailers), 65)
        self.assertEqual(m.trailers[0].id, 't211201')
        self.assertEqual(m.trailers[0].file, '258687/kinopoisk.ru-Interstellar-211201.mp4')
        self.assertEqual(m.trailers[0].preview_file, '258687/3_100619.jpg')
        self.assertEqual(m.trailers[0].dom, 'tr')

        self.assertEqual(m.genres, ['фантастика', 'драма', 'приключения'])
        self.assertEqual(m.countries, ['США', 'Великобритания'])
        self.assertGreaterEqual(m.profit_usa, 158445319)
        self.assertGreaterEqual(m.profit_russia, 24110578)
        self.assertGreaterEqual(m.profit_world, 592845319)

        # TODO: still not implemented
        # self.assertEqual(m.directors, ['Кристофер Нолан'])
        # self.assertEqual(m.scenarios, ['Джонатан Нолан', 'Кристофер Нолан'])
        # self.assertEqual(m.producers, ['Кристофер Нолан', 'Линда Обст', 'Эмма Томас'])
        # self.assertEqual(m.operators, ['Хойте Ван Хойтема'])
        # self.assertEqual(m.composers, ['Ханс Циммер'])

    def test_movie_by_id_1552(self):

        m = Movie(id=1552)
        m.get_content("main_page")
        m.get_content("trailers")

        self.assertEqual(m.profit_russia, 41000)
        self.assertEqual(m.budget, 10000000)

    def test_movie_trailers(self):
        """
        Test of movie trailers source page
        """
        m = Movie(id=521689)
        m.get_content('trailers')

        self.assertGreater(len(m.trailers), 3)
        for i in range(0, 3):
            self.assertEqual(m.trailers[i].id[0], 't')
            self.assertGreater(len(m.trailers[i].file), 0)
            self.assertGreater(len(m.trailers[i].preview_file), 0)

        self.assertEqual(m.youtube_ids, ['e4f5keHX_ks'])

    # def test_movie_repr(self):
    #     instance = Movie(title='Молчание ягнят', title_original='The Silence of the Lambs', year='1990')
    #     self.assertEqual(
    #         repr(instance),
    #         'Молчание ягнят (The Silence of the Lambs), 1990'
    #     )

    def test_movie_series(self):
        movies = Movie.objects.search('glee')
        self.assertGreaterEqual(len(movies), 1)

        m = movies[0]  # Glee / Хор / Лузеры
        self.assertTrue(m.series)
        m.get_content('series')
        self.assertGreaterEqual(len(m.seasons), 4)
        f = m.seasons[0]
        self.assertEqual(len(f.episodes), 22)
        self.assertEqual(f.year, 2010)
        e = m.seasons[0].episodes[5]
        self.assertEqual(e.title, 'Витамин D')
        self.assertEqual(e.release_date, datetime(2009, 10, 7).date())

        # It will false someday as well, we should find some TV series, that announced more series, but
        # stop showing them in some moment. At that moment, I can't find any.
        movies = Movie.objects.search('the killing')
        self.assertGreaterEqual(len(movies), 1)
        m = movies[0]  # The Killing / Убийство
        self.assertTrue(m.series)
        m.get_content('series')
        ls = m.seasons[-1]
        le = ls.episodes[-1]
        self.assertEqual(le.title, 'Эдем')
        # self.assertIsNone(le.release_date)

        m = Movie(id=419200)  # Kick-Ass / Пипец
        m.get_content('main_page')
        self.assertFalse(m.series)
        self.assertRaises(ValueError, m.get_content, ('series', ))

        m = Movie(id=306084)  # The Big Bang Theory / Теория большого взрыва
        m.get_content('main_page')
        self.assertTrue(m.series)

    def test_movie_rating(self):
        movies = Movie.objects.search('the big bang theory')
        self.assertGreaterEqual(len(movies), 1)

        m = movies[0]  # The Big Bang Theory Series
        self.assertGreaterEqual(m.rating, 8.5)

        m = Movie(id=306084)  # same
        m.get_content('main_page')
        self.assertGreaterEqual(m.rating, 8.5)


class PersonTest(unittest.TestCase):

    def test_person(self):
        """
        Test of person manager
        """
        persons = Person.objects.search('Гуальтиеро Якопетти')
        self.assertEqual(len(persons), 1)

        m = persons[0]
        self.assertEqual(m.id, 351549)
        self.assertEqual(m.name, 'Гуалтьеро Якопетти')
        self.assertEqual(m.year_birth, 1919)
        self.assertEqual(m.name_original, 'Gualtiero Jacopetti')

        persons = Person.objects.search('malkovich')
        self.assertGreater(len(persons), 1)

        m = persons[0]
        self.assertEqual(m.id, 24508)
        self.assertEqual(m.name, 'Джон Малкович')
        self.assertEqual(m.year_birth, 1953)
        self.assertEqual(m.name_original, 'John Malkovich')

        m = Person(id=6245)
        m.get_content('main_page')
        self.assertEqual(m.id, 6245)
        self.assertEqual(m.name, 'Джонни Депп')
        self.assertEqual(m.year_birth, 1963)
        self.assertEqual(m.name_original, 'Johnny Depp')
#        self.assertGreater(len(m.information), 50) # TODO: fix "Safety error" in response of subrequest

    def test_person_link_source(self):
        """
        Test of parsing person link in search results
        """
        m = Person()
        m.parse('link', """<div class="element most_wanted">
            <div class="right">
            <ul class="links">
            <li><a href="/name/24508/photos/">фото</a><s></s></li>
            <li><a href="/name/24508/sites/">сайты</a><s></s></li>
            <li><a href="/name/24508/buy/">DVD</a><s></s></li>
            <li><a href="/name/24508/relations/">связи</a><s></s></li>
            </ul>
            </div>
            <p class="pic"><a href="/name/24508/sr/1/"><img src="http://st.kp.yandex.net/images/sm_actor/24508.jpg" alt="Джон Малкович" title="Джон Малкович" /></a></p>
            <div class="info">
            <p class="name"><a href="/name/24508/sr/1/">Джон Малкович</a> <span class="year">1953</span></p>
            <span class="gray">John Malkovich</span>
            <span class="gray">
                     актер, продюсер, режиссер, сценарист
                     <br />
                     60 лет
                 </span>
            </div>
            <div class="clear"></div>
            </div>""")
        self.assertEqual(m.name, 'Джон Малкович')
        self.assertEqual(m.id, 24508)
        self.assertEqual(m.year_birth, 1953)
        self.assertEqual(m.name_original, 'John Malkovich')

    def test_person_photos_page_source(self):
        """
        Test of parsing person photos
        """
        m = Person()
        m.parse('photos', '<table class="fotos"><tr><td><a href="/picture/1294472/"><img src="http://st.kinopoisk.ru/images/kadr/sm_1294472.jpg" width="170" height="254" alt="Просмотр фото" title="Просмотр фото" /></a><b><i>1000&times;1494</i><a href="/picture/1294472/" target="_blank" title="Открыть в новом окне"></a>676 Кб</b></td><td class="center"><a href="/picture/1294471/"><img  src="http://st.kinopoisk.ru/images/kadr/sm_1294471.jpg" width="170" height="253" alt="Просмотр фото" title="Просмотр фото" /></a><b><i>1000&times;1491</i><a href="/picture/1294471/" target="_blank" title="Открыть в новом окне"></a>649 Кб</b></td></tr></table>')
        self.assertEqual(len(m.photos), 2)
        self.assertEqual(m.photos[0], '//st.kp.yandex.net/im/kadr/1/2/9/kinopoisk.ru-Johnny-Depp-1294472.jpg')

        m = Person(id=8217)
        m.get_content('photos')
        self.assertGreater(len(m.photos), 10)

    # def test_person_repr(self):
    #     instance = Person(name='Чарльз Чаплин', name_original='Charles Chaplin', year='-')
    #     self.assertEqual(
    #         repr(instance),
    #         '<Чарльз Чаплин (Charles Chaplin), ->'
    #     )

if __name__ == '__main__':
    unittest.main()
