# -*- coding: utf-8 -*-
"""
Sources for Movie
"""
from __future__ import unicode_literals

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
        'url': './/p[@class="name"]/a/@href',
        'title': './/p[@class="name"]/a/text()',
        'years': './/p[@class="name"]/span[@class="year"]/text()',
        'title_en': './/span[@class="gray"][1]/text()',
        'rating': './/div[starts-with(@class, "rating")]/@title',
    }

    def parse(self):
        self.content = html.fromstring(self.content)

        url = self.extract('url')
        title = self.extract('title', to_str=True)
        years = self.extract('years')
        title_en = self.extract('title_en', to_str=True)
        rating = self.extract('rating')

        # /level/1/film/ID/sr/1/
        self.instance.id = self.prepare_int(url.split('/')[4].split('-')[-1])
        self.instance.title = title.replace('(сериал)', '')
        self.instance.series = '(сериал)' in title

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
                if raw_date.strip().count('\xa0') == 2:
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
        'сборы в США': 'profit_usa',
        'сборы в России': 'profit_russia',
        'сборы в мире': 'profit_world',
    }

    xpath = {
        'url': './/meta[@property="og:url"]/@content',
        'title': './/h1/span/text()',
        'title_en': './/span[@itemprop="alternativeHeadline"]/text()',
        'plot': './/div[@itemprop="description"]/text()',
        'rating': './/span[@class="rating_ball"]/text()',
        'votes': './/div[@id="block_rating"]//div[@class="div1"]//span[@class="ratingCount"]/text()',
        'imdb': './/div[@id="block_rating"]//div[@class="block_2"]//div[last()]/text()',
    }

    def parse(self):
        trailers = re.findall(r'GetTrailerPreview\(([^\)]+)\)', self.content)
        if len(trailers):
            self.instance.add_trailer(json.loads(trailers[0].replace("'", '"')))

        content_info = BeautifulSoup(self.content, 'html.parser')

        table_info = content_info.find('table', {'class': re.compile(r'^info')})
        if table_info:
            for tr in table_info.findAll('tr'):
                tds = tr.findAll('td')
                name = tds[0].text
                value = tds[1].text
                if value == '-':
                    continue

                if name == 'слоган':
                    self.instance.tagline = self.prepare_str(value)
                elif name == 'время':
                    self.instance.runtime = self.prepare_int(value.split(' ')[0])
                elif name == 'год':
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
                        if genre.strip() != '... слова':
                            self.instance.genres.append(self.prepare_str(genre))
                elif name in self.main_profits:
                    self.parse_main_profit(self.main_profits[name], tds)
                elif name in self.main_persons:
                    self.parse_persons(self.main_persons[name], tds[1].contents)

        actors = content_info.find('div', {'id': 'actorList'})
        if actors and actors.ul:
            self.parse_persons('actors', [li.a for li in actors.ul.findAll('li')])

        self.content = html.fromstring(self.content)

        self.instance.id = self.prepare_int(self.extract('url').split('/')[-2].split('-')[-1])
        self.instance.title = self.extract('title', to_str=True)
        self.instance.title_en = self.extract('title_en', to_str=True)
        self.instance.plot = self.extract('plot', to_str=True)
        self.instance.rating = self.extract('rating', to_float=True)
        self.instance.votes = self.extract('votes', to_int=True)

        imdb = re.findall(r'^IMDb: ([0-9\.]+) \(([0-9 ]+)\)$', self.extract('imdb'))
        if imdb:
            self.instance.imdb_rating = float(imdb[0][0])
            self.instance.imdb_votes = self.prepare_int(imdb[0][1])

        self.instance.set_source('main_page')

    def parse_main_profit(self, field_name, value):
        setattr(self.instance, field_name, self.find_profit(value[1]))

    def parse_persons(self, field_name, links):
        from kinopoisk.person import Person
        for link in links:
            if isinstance(link, Tag) and link.text != "...":
                person = Person.get_parsed('short_link', link.decode())
                getattr(self.instance, field_name).append(person)


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

    def parse(self):
        trailers_kinopoisk_urls = list(set(
            re.findall(r'/film/{}/video/\d+'.format(self.instance.id), self.content)
        ))

        for trailer_id in trailers_kinopoisk_urls:
            trailer_id = trailer_id.split('/')[-1:][0]
            self.instance.add_trailer(trailer_id)
        youtube_urls = list(set(re.findall(r'www.youtube.com/embed/[\d\w]+', self.content)))
        youtube_ids = [youtube_id.split('/')[-1:][0] for youtube_id in youtube_urls]
        self.instance.youtube_ids = youtube_ids
        self.instance.set_source('trailers')
