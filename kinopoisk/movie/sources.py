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
    Parser movie info from person career links
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
        self.instance.id = self.extract('id')
        try:
            self.instance.imdb_rating = float(self.extract('imdb_rating'))
            self.instance.imdb_votes = int(self.extract('imdb_votes'))
        except (ValueError, TypeError):
            pass

        try:
            self.instance.rating = float(self.extract('rating'))
            self.instance.votes = self.prepare_int(self.extract('votes'))
        except (ValueError, TypeError):
            pass

        link = self.extract('link')
        role = self.extract('role').strip().split('...')
        title, year = re.findall(r'^(.+?)(?:\s+\(.*([0-9]{4})\))?$', link, re.M)[0]
        if role[0] == '':
            title = ''
            title_en = title
        else:
            title_en = role[0]

        self.instance.title = self.prepare_str(title)
        self.instance.title_en = self.prepare_str(title_en)
        if year:
            self.instance.year = self.prepare_int(year)

        self.instance.set_source('career_link')


class MoviePremierLink(KinopoiskPage):
    """
    Parser movie info from premiers links
    """

    def parse(self):

        if isinstance(self.content, Tag):
            premier_soup = self.content
        else:
            content_soup = BeautifulSoup(self.content, 'lxml')
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
    Parser movie info from links
    """
    xpath = {
        'id': './/p[@class="name"]/a/@href',
        'title': './/p[@class="name"]/a/text()',
        'years': './/p[@class="name"]/span[@class="year"]/text()',
        'name': './/span[@class="gray"]/text()',
        'rating': './/div[starts-with(@class, "rating")]/@title',
    }

    def parse(self):
        self.content = html.fromstring(self.content)

        id = self.extract('id')
        title = self.extract('title')
        years = self.extract('years')
        name = self.extract('name')
        rating = self.extract('rating')

        self.instance.id = self.prepare_int(id.split('/')[2].split('-')[-1])
        self.instance.title = self.prepare_str(title.replace('(сериал)', ''))
        self.instance.series = '(сериал)' in title

        if years:
            self.instance.year = self.prepare_int(years[:4])

        if 'мин' in name:
            values = name.split(', ')
            self.instance.runtime = self.prepare_int(values[-1].split(' ')[0])
            self.instance.title_en = self.prepare_str(', '.join(values[:-1]))
        else:
            self.instance.title_en = self.prepare_str(name)

        if rating:
            rating = rating.split(' ')
            self.instance.rating = float(rating[0])
            self.instance.votes = self.prepare_int(rating[1][1:-1])

        self.instance.set_source('link')


class MovieSeries(KinopoiskPage):
    url = '/film/{id}/episodes/'

    def parse(self):
        soup = BeautifulSoup(self.content, 'lxml')
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

    def parse(self):

        instance_id = re.compile(r'id_film = (\d+);').findall(self.content)
        if instance_id:
            self.instance.id = self.prepare_int(instance_id[0])

        content_info = BeautifulSoup(self.content, 'lxml')
        title = content_info.find('h1', {'class': 'moviename-big'})
        if title:
            self.instance.title = self.prepare_str(title.text)

        title_en = content_info.find('span', {'itemprop': 'alternativeHeadline'})

        if title_en:
            self.instance.title_en = self.prepare_str(title_en.text)

        # <div class="brand_words" itemprop="description">
        plot = content_info.find('div', {'class': 'brand_words', 'itemprop': 'description'})
        if plot:
            self.instance.plot = self.prepare_str(plot.text)

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
                        if genre != '...\nслова\n':
                            self.instance.genres.append(self.prepare_str(genre))
                elif name in self.main_profits:
                    self.parse_main_profit(self.main_profits[name], tds)
                elif name in self.main_persons:
                    self.parse_persons(self.main_persons[name], tds[1].contents)

        rating = content_info.find('span', attrs={'class': 'rating_ball'})
        if rating:
            self.instance.rating = float(rating.string)

        block_rating = content_info.find('div', attrs={'id': 'block_rating'})
        if block_rating:
            div1 = block_rating.find('div', attrs={'class': 'div1'})
            if div1:
                rating_count = div1.find('span', attrs={'class': 'ratingCount'})
                if rating_count:
                    self.instance.votes = self.prepare_int(rating_count.text)
                div_rating = div1.find_next('div')
                if div_rating:
                    imdb = re.findall(r'^IMDb: ([0-9\.]+) \(([0-9 ]+)\)$', div_rating.text)
                    if imdb:
                        self.instance.imdb_rating = float(imdb[0][0])
                        self.instance.imdb_votes = self.prepare_int(imdb[0][1])

        trailers = re.findall(r'GetTrailerPreview\(([^\)]+)\)', self.content)
        if len(trailers):
            self.instance.add_trailer(json.loads(trailers[0].replace("'", '"')))

        actors = content_info.find('div', {'id': 'actorList'})
        if actors and actors.ul:
            self.parse_persons('actors', [li.a for li in actors.ul.findAll('li')])

        self.instance.set_source('main_page')

    def parse_main_profit(self, field_name, value):
        setattr(self.instance, field_name, self.find_profit(value[1]))

    def parse_persons(self, field_name, links):
        from kinopoisk.person import Person
        for link in links:
            if isinstance(link, Tag) and link.text != "...":
                person = Person.get_parsed('short_link', link.decode())
                getattr(self.instance, field_name).append(person)


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
        trailers = re.findall(r'GetTrailerPreview\(([^\)]+)\)', self.content)
        for trailer in trailers:
            self.instance.add_trailer(json.loads(trailer.replace("'", '"')))

        self.instance.youtube_ids = list(set(re.findall(r'//www.youtube.com/v/(.+)\?', self.content)))
        self.instance.set_source(self.content_name)
