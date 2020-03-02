# -*- coding: utf-8 -*-
# flake8: noqa: E501
from __future__ import unicode_literals

from datetime import datetime

from kinopoisk.movie import Movie
from .base import BaseTest


class MovieTest(BaseTest):
    def test_movie_posters_page_source(self):
        m = Movie(id=51319)
        m.get_content('posters')
        self.assertGreaterEqual(len(m.posters), 34)

    def test_movie_search_manager_redacted(self):
        movies = Movie.objects.search('Без цензуры 2007')
        self.assertGreater(len(movies), 1)

        m = movies[0]
        self.assertEqual(m.id, 278229)
        self.assertEqual(m.year, 2007)
        self.assertEqual(m.title, 'Без цензуры')
        self.assertEqual(m.title_en, 'Redacted')
        self.assertEqual(m.runtime, 90)
        self.assertEqual(m.rating, 6.134)
        self.assertGreaterEqual(m.votes, 1760)

    def test_movie_search_manager_pulp_fiction(self):
        movies = Movie.objects.search('pulp fiction')
        self.assertGreater(len(movies), 1)

        m = movies[0]
        self.assertEqual(m.id, 342)
        self.assertEqual(m.title, 'Криминальное чтиво')
        self.assertEqual(m.year, 1994)
        self.assertEqual(m.title_en, 'Pulp Fiction')

    def test_movie_search_manager_warcraft(self):
        movies = Movie.objects.search('Варкрафт')
        self.assertEqual(len(movies), 1)

        m = movies[0]
        self.assertEqual(m.id, 277328)
        self.assertEqual(m.title, 'Варкрафт')
        self.assertEqual(m.year, 2016)
        self.assertEqual(m.title_en, 'Warcraft')

    def test_movie_main_page_id_278229(self):
        """
        Test of movie manager, movie obtain by id (not via search)
        """
        m = Movie(id=278229)
        m.get_content('main_page')
        m.get_content('trailers')

        trailers_ids = [trailer.id for trailer in m.trailers]
        trailers_files = [trailer.file for trailer in m.trailers]

        self.assertEqual(m.id, 278229)
        self.assertEqual(m.year, 2007)
        self.assertEqual(m.title, 'Без цензуры')
        self.assertEqual(m.title_en, 'Redacted')
        self.assertEqual(m.plot,
                         'В центре картины — небольшой отряд американских солдат на контрольно-пропускном пункте в Ираке. Причём восприятие их истории постоянно меняется. Мы видим события глазами самих солдат, представителей СМИ, иракцев и понимаем, как на каждого из них влияет происходящее, их встречи и столкновения друг с другом.')
        self.assertEqual(m.runtime, 90)
        self.assertEqual(m.tagline, '«Фильм, запрещенный к прокату во многих странах»')
        self.assertGreater(len(m.trailers), 3)
        self.assertIn('gettrailer.php?quality=hd&trailer_id=4476', trailers_files)
        self.assertIn('4476', trailers_ids)
        self.assertEqualPersons(m.actors, ['Иззи Диаз', 'Роб Дивейни', 'Ти Джонс', 'Анас Веллман', 'Майк Фигуроа',
                                           'Яналь Кассай', 'Дхиая Калиль', 'Кел О’Нил', 'Дэниэл Стюарт-Шерман',
                                           'Патрик Кэрролл'])

    def test_movie_main_page_id_6877(self):
        """
        Test of movie manager, movie obtain by id (not via search)
        """
        m = Movie(id=6877)
        m.get_content('main_page')
        m.get_content('trailers')

        trailers_ids = [trailer.id for trailer in m.trailers]
        trailers_files = [trailer.file for trailer in m.trailers]

        self.assertEqual(m.id, 6877)
        self.assertEqual(m.year, 2004)
        self.assertEqual(m.title, 'Терминал')
        self.assertEqual(m.title_en, 'The Terminal')
        self.assertEqual(m.plot,
                         'Фильм рассказывает историю Виктора Наворски, отправившегося в Нью-Йорк из Восточной Европы. Пока Виктор летел в самолете, на его родине произошел государственный переворот. Оказавшись в международном аэропорту имени Джона Кеннеди с паспортом ниоткуда, он не имеет права въехать в Соединенные Штаты и должен коротать свои дни и ночи на скамейках у выхода 67, пока война в его родной стране не закончится. Тянутся недели и месяцы, и Виктор обнаруживает, что небольшой мирок терминала может быть наполнен абсурдом, щедростью, амбициями, развлечениями, желанием сохранить свой статус, интуитивной прозорливостью и даже любовью к очаровательной стюардессе Амелии. Виктору удается завоевать симпатии всех, кроме одного человека — чиновника аэропорта Фрэнка Диксона, который считает его бюрократической ошибкой, проблемой, которую он не может контролировать, но от которой жаждет избавиться.')
        self.assertEqual(m.runtime, 124)

        self.assertEqual(m.rating, 8.069)
        self.assertEqual(m.imdb_rating, 7.30)
        self.assertGreaterEqual(m.votes, 214662)
        self.assertGreaterEqual(m.imdb_votes, 381282)

        self.assertEqual(m.tagline, "«Жизнь - это ожидание»")
        self.assertEqual(len(m.trailers), 4)
        self.assertIn('506', trailers_ids)
        self.assertIn('gettrailer.php?quality=hd&trailer_id=506', trailers_files)

        self.assertEqual(m.genres, ['драма', 'мелодрама', 'комедия'])
        self.assertEqual(m.countries, ['США'])
        self.assertGreaterEqual(m.budget, 60000000)
        self.assertGreaterEqual(m.marketing, 35000000)
        self.assertGreaterEqual(m.profit_usa, 77872883)
        self.assertGreaterEqual(m.profit_russia, 1880000)
        self.assertGreaterEqual(m.profit_world, 218685607)

        self.assertEqualPersons(m.actors,
                                ['Том Хэнкс', 'Кэтрин Зета-Джонс', 'Стэнли Туччи', 'Чи МакБрайд',
                                 'Диего Луна', 'Бэрри Шебака Хенли', 'Кумар Паллана', 'Зои Салдана',
                                 'Эдди Джонс', 'Джуд Чикколелла'])
        self.assertEqualPersons(m.directors, ['Стивен Спилберг'])
        self.assertEqualPersons(m.screenwriters, ['Саша Джерваси', 'Джефф Натансон', 'Эндрю Никкол'])
        self.assertEqualPersons(m.producers, ['Лори МакДональд', 'Уолтер Ф. Паркс', 'Стивен Спилберг'])
        self.assertEqualPersons(m.operators, ['Януш Камински'])
        self.assertEqualPersons(m.composers, ['Джон Уильямс'])
        self.assertEqualPersons(m.art_direction_by, ['Алекс Макдауэлл', 'Кристофер Бериэн-Мор', 'Брэд Рикер'])
        self.assertEqualPersons(m.editing_by, ['Майкл Кан'])

    def test_movie_main_page_id_1005878(self):
        """
        Test of movie manager, movie obtain by id (not via search)
        """
        m = Movie(id=1005878)
        m.get_content('main_page')

        self.assertEqual(m.id, 1005878)
        self.assertEqual(m.year, 2019)
        self.assertEqual(m.title, 'Король Лев')
        self.assertEqual(m.title_en, 'The Lion King')
        self.assertEqual(m.plot,
                         'История об отважном львенке по имени Симба. Знакомые с детства герои взрослеют, влюбляются, познают себя и окружающий мир, совершают ошибки и делают правильный выбор.')
        self.assertEqual(m.runtime, 118)

        self.assertEqual(m.rating, 7.158)
        self.assertEqual(m.imdb_rating, 6.90)
        self.assertGreaterEqual(m.votes, 60604)
        self.assertGreaterEqual(m.imdb_votes, 169531)

        self.assertEqual(m.tagline, "«The King Has Returned»")

        self.assertEqual(m.genres, ['мультфильм', 'мюзикл', 'драма', 'приключения', 'семейный'])
        self.assertEqual(m.countries, ['США'])
        self.assertGreaterEqual(m.budget, 260000000)
        self.assertIsNone(m.marketing)
        self.assertGreaterEqual(m.profit_usa, 543638043)
        self.assertGreaterEqual(m.profit_russia, 47106883)
        self.assertGreaterEqual(m.profit_world, 1656943394)

        self.assertEqualPersons(m.actors,
                                ['Джеймс Эрл Джонс', 'Дональд Гловер', 'Чиветель Эджиофор', 'Джон Оливер',
                                 'Джон Кани', 'Элфри Вудард', 'Джейдон Маккрэри', 'Шахади Райт Джозеф',
                                 'Пенни Джонсон', 'Кигэн-Майкл Ки'])
        self.assertEqualPersons(m.directors, ['Джон Фавро'])
        self.assertEqualPersons(m.screenwriters, ['Джефф Натансон', 'Ирен Меччи', 'Джонатан Робертс'])
        self.assertEqualPersons(m.producers, ['Джон Бартники', 'Дэбби Босси', 'Джон Фавро'])
        self.assertEqualPersons(m.operators, ['Калеб Дешанель'])
        self.assertEqualPersons(m.composers, ['Ханс Циммер'])
        self.assertEqualPersons(m.art_direction_by, ['Джеймс Чинланд', 'Влад Бина'])
        self.assertEqualPersons(m.editing_by, ['Адам Герстл', 'Марк Ливолси'])

    def test_movie_main_page_id_746251(self):
        m = Movie(id=746251)
        m.get_content('main_page')
        self.assertEqual(m.year, None)
        self.assertEqual(m.title, 'Ловкость')

        self.assertEqual(m.genres, ['драма'])
        self.assertEqual(m.countries, ['США'])

    def test_movie_main_page_empty_actors(self):
        m = Movie(id=926005)
        m.get_content('main_page')
        self.assertEqual(m.actors, [])

    def test_movie_main_page_id_4374(self):
        """
        Test of movie manager, movie obtain by id (not via search)
        """
        m = Movie(id=4374)
        m.get_content('main_page')
        m.get_content('trailers')

        trailers_ids = [trailer.id for trailer in m.trailers]
        trailers_files = [trailer.file for trailer in m.trailers]

        self.assertEqual(m.id, 4374)
        self.assertEqual(m.year, 2003)
        self.assertEqual(m.title, 'Пираты Карибского моря: Проклятие Черной жемчужины')
        self.assertEqual(m.title_en, 'Pirates of the Caribbean: The Curse of the Black Pearl')
        self.assertEqual(m.plot,
                         'Жизнь харизматичного авантюриста, капитана Джека Воробья, полная увлекательных приключений, резко меняется, когда его заклятый враг — капитан Барбосса — похищает корабль Джека, Черную Жемчужину, а затем нападает на Порт Ройал и крадет прекрасную дочь губернатора, Элизабет Свонн. Друг детства Элизабет, Уилл Тернер, вместе с Джеком возглавляет спасательную экспедицию на самом быстром корабле Британии, в попытке вызволить девушку из плена и заодно отобрать у злодея Черную Жемчужину. Вслед за этой парочкой отправляется амбициозный коммодор Норрингтон, который к тому же числится женихом Элизабет. Однако Уилл не знает, что над Барбоссой висит вечное проклятие, при лунном свете превращающее его с командой в живых скелетов. Проклятье будет снято лишь тогда, когда украденное золото Ацтеков будет возвращено пиратами на старое место.')
        self.assertEqual(m.runtime, 143)

        self.assertEqual(m.rating, 8.335)
        self.assertEqual(m.imdb_rating, 8.00)
        self.assertGreaterEqual(m.votes, 327195)
        self.assertGreaterEqual(m.imdb_votes, 859395)

        self.assertEqual(m.tagline,
                         "«Over 3000 Islands of Paradise -- For Some it's A Blessing -- For Others... It's A Curse»")
        self.assertGreater(len(m.trailers), 2)
        self.assertTrue('529' in trailers_ids)
        self.assertTrue('gettrailer.php?quality=hd&trailer_id=529' in trailers_files)

        self.assertEqual(m.genres, ['фэнтези', 'боевик', 'приключения'])
        self.assertEqual(m.countries, ['США'])
        self.assertGreaterEqual(m.budget, 140000000)
        self.assertGreaterEqual(m.marketing, 40000000)
        self.assertGreaterEqual(m.profit_usa, 305413918)
        self.assertGreaterEqual(m.profit_russia, 9060000)
        self.assertGreaterEqual(m.profit_world, 654264015)

        self.assertEqualPersons(m.actors,
                                ['Джонни Депп', 'Джеффри Раш', 'Орландо Блум', 'Кира Найтли', 'Джек Девенпорт',
                                 'Кевин МакНэлли', 'Джонатан Прайс', 'Ли Аренберг', 'Макензи Крук', 'Дэвид Бэйли'])
        self.assertEqualPersons(m.directors, ['Гор Вербински'])
        self.assertEqualPersons(m.screenwriters, ['Тед Эллиот', 'Терри Россио', 'Стюарт Битти'])
        self.assertEqualPersons(m.producers, ['Джерри Брукхаймер', 'Пол Дисон', 'Брюс Хендрикс'])
        self.assertEqualPersons(m.operators, ['Дариуш Вольски'])
        self.assertEqualPersons(m.composers, ['Клаус Бадельт'])
        self.assertEqualPersons(m.art_direction_by, ['Брайан Моррис', 'Дерек Р. Хилл', 'Майкл Пауэлс'])
        self.assertEqualPersons(m.editing_by, ['Стивен Е. Ривкин', 'Артур Шмидт', 'Крэйг Вуд'])

    def test_movie_main_page_id_258687(self):
        """
        Test of movie manager, movie obtain by id (not via search)
        """
        m = Movie(id=258687)
        m.get_content('main_page')
        m.get_content('trailers')

        trailers_ids = [trailer.id for trailer in m.trailers]
        trailers_files = [trailer.file for trailer in m.trailers]

        self.assertEqual(m.id, 258687)
        self.assertEqual(m.year, 2014)
        self.assertEqual(m.title, 'Интерстеллар')
        self.assertEqual(m.title_en, 'Interstellar')
        self.assertEqual(m.plot,
                         'Когда засуха приводит человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину (которая предположительно соединяет области пространства-времени через большое расстояние) в путешествие, чтобы превзойти прежние ограничения для космических путешествий человека и переселить человечество на другую планету.')
        self.assertEqual(m.runtime, 169)
        self.assertEqual(m.tagline, '«Следующий шаг человечества станет величайшим»')

        self.assertGreater(len(m.trailers), 70)
        self.assertTrue('109352' in trailers_ids)
        self.assertTrue('gettrailer.php?quality=hd&trailer_id=109352'in trailers_files)

        self.assertEqual(m.genres, ['фантастика', 'драма', 'приключения'])
        self.assertEqual(m.countries, ['США', 'Великобритания', 'Канада'])
        self.assertGreaterEqual(m.profit_usa, 158445319)
        self.assertGreaterEqual(m.profit_russia, 24110578)
        self.assertGreaterEqual(m.profit_world, 592845319)

        self.assertEqualPersons(m.directors, ['Кристофер Нолан'])
        self.assertEqualPersons(m.screenwriters, ['Джонатан Нолан', 'Кристофер Нолан'])
        self.assertEqualPersons(m.producers, ['Кристофер Нолан', 'Линда Обст', 'Эмма Томас'])
        self.assertEqualPersons(m.operators, ['Хойте Ван Хойтема'])
        self.assertEqualPersons(m.composers, ['Ханс Циммер'])

    def test_movie_by_id_1552(self):
        m = Movie(id=1552)
        m.get_content('main_page')
        # m.get_content('trailers')

        self.assertEqual(m.profit_russia, 41000)
        self.assertEqual(m.budget, 10000000)

    def test_movie_trailers(self):
        """
        Test of movie trailers source page
        """
        m = Movie(id=521689)
        m.get_content('trailers')

        self.assertGreaterEqual(len(m.trailers), 11)
        trailers_ids = [trailer.id for trailer in m.trailers]
        trailers_files = [trailer.file for trailer in m.trailers]

        self.assertTrue('76485' in trailers_ids)
        self.assertTrue('gettrailer.php?quality=hd&trailer_id=76485' in trailers_files)

        self.assertTrue('74666' in trailers_ids)
        self.assertTrue('gettrailer.php?quality=hd&trailer_id=74666' in trailers_files)
        self.assertEqual(m.youtube_ids, ['e4f5keHX_ks'])

    def test_movie_cast(self):
        """
        Test of movie cast source page
        """
        m = Movie(id=4220)
        m.get_content('cast')

        self.assertEqual(len(m.cast), 7)
        self.assertGreaterEqual(len(m.cast['director']), 1)
        self.assertGreaterEqual(len(m.cast['actor']), 49)
        self.assertGreaterEqual(len(m.cast['producer']), 4)
        self.assertGreaterEqual(len(m.cast['writer']), 3)
        self.assertGreaterEqual(len(m.cast['operator']), 2)
        self.assertGreaterEqual(len(m.cast['design']), 1)
        self.assertGreaterEqual(len(m.cast['editor']), 1)

        self.assertEqual(m.cast['actor'][0].person.id, 8986)
        self.assertEqual(m.cast['actor'][0].person.name, 'Питер Фонда')
        self.assertEqual(m.cast['actor'][0].person.name_en, 'Peter Fonda')
        self.assertEqual(m.cast['actor'][0].name, 'Wyatt')

        # в титрах: ...
        self.assertEqual(m.cast['actor'][13].person.name, 'Сэнди Браун Уайет')
        self.assertEqual(m.cast['actor'][13].person.name_en, 'Sandy Brown Wyeth')
        self.assertEqual(m.cast['actor'][13].name, 'Joanne')

    def test_movie_cast_1(self):
        """
        Test of movie cast source page
        """
        m = Movie(id=63991)
        m.get_content('cast')

        self.assertEqual(len(m.cast), 11)
        self.assertGreaterEqual(len(m.cast['director']), 1)
        self.assertGreaterEqual(len(m.cast['actor']), 49)
        self.assertGreaterEqual(len(m.cast['producer']), 4)
        self.assertGreaterEqual(len(m.cast['voice_director']), 1)
        self.assertGreaterEqual(len(m.cast['translator']), 1)
        self.assertGreaterEqual(len(m.cast['voice']), 4)
        self.assertGreaterEqual(len(m.cast['writer']), 3)
        self.assertGreaterEqual(len(m.cast['operator']), 1)
        self.assertGreaterEqual(len(m.cast['composer']), 1)
        self.assertGreaterEqual(len(m.cast['design']), 1)
        self.assertGreaterEqual(len(m.cast['editor']), 1)

        # with $
        self.assertEqual(m.cast['actor'][0].person.id, 6245)
        self.assertEqual(m.cast['actor'][0].person.name, 'Джонни Депп')
        self.assertEqual(m.cast['actor'][0].person.name_en, 'Johnny Depp')
        self.assertEqual(m.cast['actor'][0].name, 'Jack Sparrow')

        # no mention
        self.assertEqual(m.cast['actor'][16].person.id, 24683)
        self.assertEqual(m.cast['actor'][16].name, 'Captain Hector Barbossa')

        # voice
        self.assertEqual(m.cast['actor'][63].person.id, 288908)
        self.assertEqual(m.cast['actor'][63].name, 'Parrot')
        self.assertEqual(m.cast['actor'][63].voice, True)

        # with $ and no name
        self.assertEqual(m.cast['producer'][0].name, '')

    def test_movie_repr(self):
        instance = Movie(title='Молчание ягнят', title_en='The Silence of the Lambs', year='1990')
        self.assertEqual(instance.__repr__(), 'Молчание ягнят (The Silence of the Lambs), 1990')

    def test_movie_series_search_glee(self):
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
        self.assertEqual(e.release_date, datetime(2010, 11, 20).date())

    def test_movie_series_search_killing(self):
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

    def test_movie_series_main_page_kickass(self):
        m = Movie(id=419200)  # Kick-Ass / Пипец
        m.get_content('main_page')
        self.assertFalse(m.series)
        self.assertRaises(ValueError, m.get_content, ('series',))

    def test_movie_series_main_page_bigband(self):
        m = Movie(id=306084)  # The Big Bang Theory / Теория большого взрыва
        m.get_content('main_page')
        self.assertTrue(m.series)

    def test_movie_rating_from_search_result(self):
        movies = Movie.objects.search('the big bang theory')
        self.assertGreaterEqual(len(movies), 1)

        m = movies[0]  # The Big Bang Theory Series
        self.assertGreaterEqual(m.rating, 8.5)
