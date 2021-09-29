# -*- coding: utf-8 -*-
"""
Sources for Movie
"""
import re
import simplejson as json
from bs4 import BeautifulSoup, Tag
from dateutil import parser
from lxml import html

from ..utils import KinopoiskPage, KinopoiskImagesPage


class MovieCareerLink(KinopoiskPage):
    """
    Parser of movie info in person career link
    """
    xpath = {
        'id': './/@data-fid',
        'imdb_rating': './/@data-imdbr',
        'imdb_votes': './/@data-imdbv',
        'rating': './/div[@class="rating kp"]/a/text()',
        'votes': './/div[@class="rating kp"]/span/text()',
        'link': './/span[@class="name"]/a/text()',
        'role': './/span[@class="role"]/text()',
    }

    def parse(self):
        self.instance.id = self.extract('id', to_int=True)
        self.instance.imdb_rating = self.extract('imdb_rating', to_float=True)
        self.instance.imdb_votes = self.extract('imdb_votes', to_int=True)
        self.instance.rating = self.extract('rating', to_float=True)
        self.instance.votes = self.extract('votes', to_int=True)

        link = self.extract('link', to_str=True)
        role = self.extract('role', to_str=True)
        title, movie_type, year = re.findall(r'^(.+?)(?:\s+\((.*)([0-9]{4}|\.\.\.)\))?(?: Top250: \d+)?$', link, re.M)[0]

        role = self.split_triple_dots(role)
        if role[0] == '':
            title_en = title
            title = ''
        else:
            title_en = role[0]

        self.instance.title = self.prepare_str(title)
        self.instance.title_en = self.prepare_str(title_en)
        self.instance.series = 'сериал' in movie_type
        if year and not self.instance.series:
            self.instance.year = self.prepare_int(year)
        elif self.instance.series:
            series_start = re.findall(r'[0-9]{4}', movie_type)
            if series_start:
                start = self.prepare_int(series_start[0])
                if year != '...':
                    self.instance.series_years = (start, self.prepare_int(year))
                else:
                    self.instance.series_years = (start,)

        self.instance.set_source('career_link')


class MoviePremierLink(KinopoiskPage):
    """
    Parser of movie info from premiers links
    """

    def parse(self):

        if isinstance(self.content, Tag):
            premier_soup = self.content
        else:
            content_soup = BeautifulSoup(self.content, 'html.parser')
            premier_soup = content_soup.find('div', {'class': 'premier_item'})

        title_soup = premier_soup.find('span', {'class': 'name_big'}) or premier_soup.find('span', {'class': 'name'})

        self.instance.id = self.prepare_int(premier_soup['id'])
        self.instance.title = self.prepare_str(title_soup.find('a').contents[0])
        date = premier_soup.find('meta', {'itemprop': 'startDate'})['content']
        try:
            self.instance.release = parser.parse(date)
        except Exception:
            pass

        match = re.findall(r'^(.+) \((\d{4})\)$', title_soup.nextSibling.nextSibling.contents[0])
        if len(match):
            self.instance.title_en = self.prepare_str(match[0][0].strip())
            self.instance.year = self.prepare_int(match[0][1])

        try:
            self.instance.plot = self.prepare_str(premier_soup.find('span', {'class': 'sinopsys'}).contents[0])
        except Exception:
            pass

        self.instance.set_source('premier_link')


class MovieLink(KinopoiskPage):
    """
    Parser of movie info in link
    """
    xpath = {
        'url': './/p[@class="name"]/a/@data-url',
        'title': './/p[@class="name"]/a/text()',
        'years': './/p[@class="name"]/span[@class="year"]/text()',
        'title_en': './/span[@class="gray"][1]/text()',
        'rating': './/div[starts-with(@class, "rating")]/@title',
    }

    def parse(self):
        self.content = html.fromstring(self.content)

        url = self.extract('url')
        years = self.extract('years')
        title_en = self.extract('title_en', to_str=True)
        rating = self.extract('rating')

        self.instance.id = self.prepare_int(url.split('/')[2])
        self.instance.title = self.extract_title()
        self.instance.series = 'сериал' in self.extract('title')

        if years:
            self.instance.year = self.prepare_int(years[:4])

        if 'мин' in title_en:
            values = title_en.split(', ')
            self.instance.runtime = self.prepare_int(values[-1].split(' ')[0])
            self.instance.title_en = ', '.join(values[:-1])
        else:
            self.instance.title_en = title_en

        if rating:
            rating = rating.split(' ')
            self.instance.rating = float(rating[0])
            self.instance.votes = self.prepare_int(rating[1][1:-1])

        self.instance.set_source('link')


class MovieSeries(KinopoiskPage):
    url = '/film/{id}/episodes/'

    def parse(self):
        soup = BeautifulSoup(self.content, 'html.parser')
        for season in soup.findAll('h1', attrs={'class': 'moviename-big'}):
            if '21px' not in season['style']:
                continue

            parts = season.nextSibling.split(',')
            if len(parts) == 2:
                year = self.prepare_int(parts[0])
            tbody = season.parent.parent.parent
            episodes = []
            for tr in tbody.findAll('tr')[1:]:
                if not tr.find('h1'):
                    continue

                raw_date = tr.find('td', attrs={'width': '20%'}).string
                if raw_date.strip().count(' ') == 2:
                    normalized_date = self.prepare_date(raw_date)
                else:
                    normalized_date = raw_date
                title = tr.find('h1').b.string
                if title.startswith('Эпизод #'):
                    title = None
                episodes.append((title, normalized_date))

            if episodes:
                self.instance.add_series_season(year, episodes)


class MovieMainPage(KinopoiskPage):
    """
    Parser of main movie page
    """
    url = '/film/{id}/'
    main_persons = {
        'режиссер': 'directors',
        'сценарий': 'screenwriters',
        'продюсер': 'producers',
        'оператор': 'operators',
        'композитор': 'composers',
        'художник': 'art_direction_by',
        'монтаж': 'editing_by',
    }
    main_profits = {
        'бюджет': 'budget',
        'маркетинг': 'marketing',
        'сборы в сша': 'profit_usa',
        'сборы в россии': 'profit_russia',
        'сборы в мире': 'profit_world',
    }

    xpath = {
        'url': './/meta[@property="og:url"]/@content',
        'title': './/h1/span/text()',
        'title_en': './/span[@class="styles_originalTitle__19q6I"]/text()',
        'plot': './/p[@class="styles_paragraph__2Otvx"]/text()',
        'rating': '(.//span[contains(@class,"film-rating-value")])[1]/text()',
        'votes': '(.//span[@class="styles_count__3hSWL"])[2]/text()',
        'imdb': './/div[contains(@class," film-sub-rating")]/span[1]/text()[3]',
        'imdb2': './/div[contains(@class," film-sub-rating")]/span[2]/text()',
    }

    regex = {
        'trailers': re.compile(r'GetTrailerPreview\(([^)]+)\)'),
        'imdb': re.compile(r'^IMDb: ([0-9.]+) \(([0-9 ]+)\)$'),
    }

    def parse(self):
        content_info = BeautifulSoup(self.content, 'html.parser')

        table_info = content_info.find('div', {'data-test-id': 'encyclopedic-table'})
        if table_info:
            self.parse_table_info(table_info)

        trailers = self.regex['trailers'].findall(self.content)
        if len(trailers):
            self.instance.add_trailer(json.loads(trailers[0].replace("'", '"')))

        self.parse_actors(content_info)

        self.content = html.fromstring(self.content)

        self.instance.id = self.prepare_int(self.extract('url').split('/')[-2].split('-')[-1])
        self.instance.title = self.extract_title()
        self.instance.title_en = self.extract('title_en', to_str=True)
        self.instance.plot = self.extract('plot', to_str=True)
        self.instance.plot = re.sub(r'\s+', ' ', self.instance.plot)
        try:
            self.instance.rating = self.extract('rating', to_float=True)
        except ValueError:
            # https://www.kinopoisk.ru/film/926005/
            # ValueError: could not convert string to float: '98%'
            pass

        self.instance.votes = self.extract('votes', to_int=True)
        self.instance.imdb_rating = self.extract('imdb', to_float=True)
        imdb_votes = self.extract('imdb2')
        if imdb_votes:
            if 'K' in imdb_votes:
                imdb_votes = imdb_votes.replace('K', '') * 100000
            self.instance.imdb_votes = self.prepare_int(imdb_votes)

        self.instance.set_source('main_page')

    def parse_table_info(self, table_info):
        for row in table_info.findChildren('div', recursive=False):
            pairs = row.findChildren('div')
            name = pairs[0].text
            value = pairs[1]
            self.set_value(name, value)

    def parse_main_profit(self, field_name, value):
        setattr(self.instance, field_name, self.find_profit(value))

    def parse_actors(self, content_info):
        container = content_info.find('div', {'class': re.compile(r'film-crew')}).find('ul')
        if container:
            actors = container.parent
            if actors and actors.ul:
                self.parse_persons('actors', [li.a for li in actors.ul.findAll('li')])

    def parse_persons(self, field_name, links):
        from kinopoisk.person import Person
        for link in links:
            if isinstance(link, Tag) and link.text != "...":
                person = Person.get_parsed('short_link', link.decode())
                getattr(self.instance, field_name).append(person)

    def set_value(self, name, value_tds):
        value = value_tds.text
        if value == '-':
            return
        name = name.lower()

        if name == 'слоган':
            self.instance.tagline = self.prepare_str(value)
        elif name == 'время':
            if value != '—':
                self.instance.runtime = self.prepare_int(value.split(' ')[0])
        elif name in ['год', 'год производства']:
            try:
                self.instance.year = self.prepare_int(value.split('(')[0])
            except ValueError:
                pass
            self.instance.series = 'сезон' in value
        elif name == 'страна':
            for item in value.split(', '):
                self.instance.countries.append(self.prepare_str(item))
        elif name == 'жанр':
            genres = value.split(', ')
            for genre in genres:
                self.instance.genres.append(self.prepare_str(genre.replace('слова', '')))
        elif name in self.main_profits:
            self.parse_main_profit(self.main_profits[name], value_tds)
        elif name in self.main_persons:
            self.parse_persons(self.main_persons[name], value_tds.contents)


class MovieCastPage(KinopoiskPage):
    """
    Parser of kinopoisk movie cast page
    """
    url = '/film/{id}/cast/'

    xpath = {
        'persons': '//div[@class="actorInfo"]',
    }

    def parse(self):
        self.content = html.fromstring(self.content)

        # persons
        from kinopoisk.movie import Role
        for element in self.extract('persons'):
            type = self.get_type(element)
            self.instance.cast.setdefault(type, [])
            self.instance.cast[type].append(Role.get_parsed('role_link', element))

        self.instance.set_source('cast')

    def get_type(self, element):
        type_el = element.getparent()
        while True:
            type_el = type_el.getprevious()
            if type_el.tag == 'a':
                return type_el.attrib['name']


class MovieRoleLink(KinopoiskPage):
    """
    Parser of movie role info in movie cast link
    """
    xpath = {
        'note': './/div[@class="role"]/text()',
    }

    def parse(self):
        from kinopoisk.person import Person
        note = self.extract('note', to_str=True).split('...')
        role_name = None
        if len(note) > 1:
            role_name = re.sub(r'^(.*),( в титрах не указан.?| озвучка)?$', r'\1', self.prepare_str(note[1]))
            if 'озвучка' in note[1]:
                self.instance.voice = True

        self.instance.name = role_name
        self.instance.person = Person.get_parsed('cast_link', self.content)

        self.instance.set_source('role_link')


class MoviePostersPage(KinopoiskImagesPage):
    """
    Parser of movie posters page
    """
    url = '/film/{id}/posters/'
    field_name = 'posters'


class MovieTrailersPage(KinopoiskPage):
    """
    Parser of kinopoisk trailers page
    """
    url = '/film/{id}/video/'

    xpath = {
        'trailers': '//a[@class="all" and contains(@href, "film/")]',
    }

    def parse(self):
        youtube_urls = list(set(re.findall(r'www.youtube.com/embed/[\d\w]+', self.content)))
        youtube_ids = [youtube_id.split('/')[-1:][0] for youtube_id in youtube_urls]
        self.instance.youtube_ids = youtube_ids

        self.content = html.fromstring(self.content)

        for element in self.extract('trailers'):
            element_id = element.get('href').split('/')[-2]
            self.instance.add_trailer(element_id)

        self.instance.set_source('trailers')


class MovieLikePage(KinopoiskPage):
    """
    Parser of kinopoisk movie like page
    """
    url = '/film/{id}/like/'

    xpath = {
        'films': '//a[@class="all" and contains(@href, "film/")]',
    }

    def parse(self):
        self.content = html.fromstring(self.content)
        self.instance.similar_movies = []

        for element in self.extract('films'):
            element_id = element.get('href').split('/')[-2]
            self.instance.similar_movies.append(element_id)

        self.instance.set_source('similar_movies')
