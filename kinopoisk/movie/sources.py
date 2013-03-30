# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup, Tag
from dateutil import parser

import simplejson as json
import re

from kinopoisk.utils import KinopoiskPage, KinopoiskImagesPage

class SeriesEpisode(object):
    def __init__(self, title=None, release_date=None):
        self.title = title
        self.release_date = release_date

    def __repr__(self):
        return '<%s "%s", %s>' % (
            self.__class__.__name__,
            self.title.encode('utf-8') if self.title else '???',
            self.release_date or '-'
        )

class SeriesSeason(object):
    def __init__(self, year, episodes=[]):
        self.year = year
        self.episodes = episodes

    def __repr__(self):
        return '<%s of %d: %d>' % (self.__class__, self.year, len(self.episodes))

class MoviePremierLink(KinopoiskPage):
    '''
    Parser movie info from premiers links
    '''
    def parse(self, instance, content):

        if isinstance(content, Tag):
            premier_soup = content
        else:
            content_soup = BeautifulSoup(content)
            premier_soup = content_soup.find('div', {'class': 'premier_item'})

        title_soup = premier_soup.find('span', {'class': 'name_big'}) or premier_soup.find('span', {'class': 'name'})

        instance.id = self.prepare_int(premier_soup['id'])
        instance.title = self.prepare_str(title_soup.find('a').contents[0])
        date = premier_soup.find('meta', {'itemprop': 'startDate'})['content']
        try:
            instance.release = parser.parse(date)
        except:
            pass

        match = re.findall(r'^(.+) \((\d{4})\)$', title_soup.nextSibling.nextSibling.contents[0])
        if len(match):
            instance.title_original = self.prepare_str(match[0][0].strip())
            instance.year = self.prepare_int(match[0][1])

        try:
            instance.plot = self.prepare_str(premier_soup.find('span', {'class': 'sinopsys'}).contents[0])
        except:
            pass

        instance.set_source('premier_link')

class MovieLink(KinopoiskPage):
    '''
    Parser movie info from links
    '''
    def parse(self, instance, content):
        content_soup = BeautifulSoup(content)

        link = content_soup.find('p', {'class': 'name'})
        if link:
            link = link.find('a')
            if link:
                # /level/1/film/342/sr/1/
                instance.id = self.prepare_int(link['href'].split('/')[4])
                instance.title = self.prepare_str(link.text)
                instance.series = u'(сериал)' in instance.title

        year = content_soup.find('p', {'class': 'name'})
        if year:
            year = year.find('span', {'class': 'year'})
            if year:
                # '1998 &ndash; 2009'
                instance.year = self.prepare_int(year.text[:4])

        otitle = content_soup.find('span', {'class': 'gray'})
        if otitle:
            if u'мин' in otitle.text:
                values = otitle.text.split(', ')
                instance.runtime = self.prepare_int(values[-1].split(' ')[0])
                instance.title_original = self.prepare_str(', '.join(values[:-1]))
            else:
                instance.title_original = self.prepare_str(otitle.text)

        rating = content_soup.find('div', attrs={'class': 'rating'})
        if rating:
            instance.rating = float(rating['title'].split(' ')[0])

        instance.set_source('link')

class MovieSeries(KinopoiskPage):
    url = '/film/%s/episodes/'

    def parse(self, instance, content):
        soup = BeautifulSoup(content, convertEntities=BeautifulSoup.ALL_ENTITIES)
        for season in soup.findAll('h1', attrs={'class': 'moviename-big'}):
            if '21px' not in season['style']:
                continue



            year = self.prepare_int(season.nextSibling.split(',')[0])
            tbody = season.parent.parent.parent
            episodes = []
            for tr in tbody.findAll('tr')[1:]:
                if not tr.find('h1'):
                    continue

                raw_date = tr.find('td', attrs={'width': '20%'}).string
                normalized_date = self.prepare_date(raw_date)
                title = tr.find('h1').b.string
                if title.startswith(u'Эпизод #'):
                    title = None
                episodes.append(SeriesEpisode(title, normalized_date))

            if episodes:
                instance.seasons.append(SeriesSeason(year, episodes))

class MovieMainPage(KinopoiskPage):
    '''
    Parser of main movie page
    '''
    url = '/film/%d/'

    def parse(self, instance, content):

        instance_id = re.compile(r'<script type="text/javascript"> id_film = (\d+); </script>').findall(content)
        if instance_id:
            instance.id = self.prepare_int(instance_id[0])

        content_info = BeautifulSoup(content)
        title = content_info.find('h1', {'class': 'moviename-big'})
        if title:
            instance.title = self.prepare_str(title.text)

        title_original = content_info.find('span', {'style': 'color: #666; font-size: 13px'})
        if title_original:
            instance.title_original = self.prepare_str(title_original.text)

        # <div class="brand_words" itemprop="description">
        plot = content_info.find('div', {'class': 'brand_words', 'itemprop': 'description'})
        if plot:
            instance.plot = self.prepare_str(plot.text)

        table_info = content_info.find('table', {'class': 'info'})
        if table_info:
            for tr in table_info.findAll('tr'):
                tds = tr.findAll('td')
                name = tds[0].text
                value = tds[1].text
                if value == '-':
                    continue

                if name == u'слоган':
                    instance.tagline = self.prepare_str(value)
                elif name == u'время':
                    instance.runtime = self.prepare_int(value.split(' ')[0])
                elif name == u'год':
                    instance.year = self.prepare_int(value[:4])
                    instance.series = u'сезон' in value

        rating = content_info.find('span', attrs={'class': 'rating_ball'})
        if rating:
            instance.rating = float(rating.string)

        trailers = re.findall(r'GetTrailerPreview\(([^\)]+)\)', content)
        if len(trailers):
            instance.add_trailer(json.loads(trailers[0].replace("'",'"')))

        instance.set_source('main_page')

class MoviePostersPage(KinopoiskImagesPage):
    '''
    Parser of movie posters page
    '''
    url = '/film/%d/posters/'
    field_name = 'posters'

class MovieTrailersPage(KinopoiskPage):
    '''
    Parser of kinopoisk trailers page
    '''
    url = '/film/%d/video/'

    def parse(self, instance, content):
        trailers = re.findall(r'GetTrailerPreview\(([^\)]+)\)', content)
        for trailer in trailers:
            instance.add_trailer(json.loads(trailer.replace("'",'"')))

        instance.set_source(self.content_name)
