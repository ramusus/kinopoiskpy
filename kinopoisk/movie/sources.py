# -*- coding: utf-8 -*-
import re

from BeautifulSoup import BeautifulSoup, Tag
from dateutil import parser

from kinopoisk.utils import KinopoiskPage, KinopoiskImagesPage

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

        instance.set_source('link')

class MovieMainPage(KinopoiskPage):
    '''
    Parser of main movie page
    '''
    url = '/level/1/film/%d/'

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

        instance.set_source('main_page')

class MoviePostersPage(KinopoiskImagesPage):
    '''
    Parser of movie posters page
    '''
    url = '/level/17/film/%d/'
    field_name = 'posters'
