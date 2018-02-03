# -*- coding: utf-8 -*-
"""
Sources for Person
"""
from __future__ import unicode_literals

import re
from builtins import str
from lxml import html

from ..utils import KinopoiskPage, KinopoiskImagesPage, HEADERS


class PersonRoleLink(KinopoiskPage):
    """
    Parser person role info from career list
    """
    xpath = {
        'note': './/span[@class="role"]/text()',
    }

    def parse(self):
        from kinopoisk.movie import Movie
        note = self.extract('note').strip().split('...')
        role_name = None
        if len(note) > 1:
            role_name = self.prepare_str(note[1]).replace(', озвучка', '').replace('; короткометражка', '')

        self.instance.name = role_name
        self.instance.movie = Movie.get_parsed('career_link', self.content)

        self.instance.set_source('role_link')


class PersonShortLink(KinopoiskPage):
    """
    Parser person info from short links
    """

    def parse(self):
        link = re.compile(r'<a[^>]+href="/name/(\d+)/">(.+?)</a>').findall(self.content)
        if link:
            self.instance.id = self.prepare_int(link[0][0])
            self.instance.name = self.prepare_str(link[0][1])

        self.instance.set_source('short_link')


class PersonLink(KinopoiskPage):
    """
    Parser person info from links
    """
    xpath = {
        'link': './/p[@class="name"]/a',
        'years': './/span[@class="year"]/text()',
        'name': './/span[@class="gray"]/text()',
    }

    def parse(self):
        self.content = html.fromstring(self.content)

        link = self.extract('link')[0]
        years = self.extract('years')
        name = self.extract('name')

        self.instance.id = self.prepare_int(link.get('href').split('/')[2])
        self.instance.name = self.prepare_str(link.text)
        self.instance.name_en = self.prepare_str(name)
        if years:
            years = years.split(' \u2013 ')
            self.instance.year_birth = self.prepare_int(years[0])
            if len(years) > 1:
                self.instance.year_death = self.prepare_int(years[1])

        self.instance.set_source('link')


class PersonMainPage(KinopoiskPage):
    """
    Parser of main person page
    """
    url = '/name/{id}/'
    xpath = {
        'movies': '//div[@class="personPageItems"]/div[@class="item"]',
    }

    def parse(self):

        person_id = re.compile(r"<link rel=\"canonical\" href=\"https?://www.kinopoisk.ru/name/(\d+)/\" />").findall(
            self.content)
        if person_id:
            self.instance.id = self.prepare_int(person_id[0])

        name = re.compile(r'<h1 class="moviename-big" itemprop="name">(.+?)</h1>').findall(self.content)
        if name:
            self.instance.name = self.prepare_str(name[0])

        name_en = re.compile(r'<span itemprop="alternateName">([A-Z]\'?[- a-zA-Z]+)</span>').findall(self.content)
        if name_en:
            self.instance.name_en = self.prepare_str(name_en[0])

        content_info = re.compile(r'<tr\s*>\s*<td class="type">(.+?)</td>\s*<td[^>]*>(.+?)</td>\s*</tr>').findall(
            self.content)
        for name, value in content_info:
            if str(name) == 'дата рождения':
                year_birth = re.compile(r'<a href="/lists/m_act%5Bbirthday%5D%5Byear%5D/\d{4}/">(\d{4})</a>').findall(
                    value)
                if year_birth:
                    self.instance.year_birth = self.prepare_int(year_birth[0])

        if self.instance.id:
            token = re.findall(r'xsrftoken = \'([^\']+)\'', self.content)
            obj_type = re.findall(r'objType: \'([^\']+)\'', self.content)
            if token and obj_type:
                response = self.request.get(self.instance.get_url('info', token=token[0], type=obj_type[0]), headers=HEADERS)
                response.connection.close()
                if response.content:
                    self.instance.information = response.content.decode('windows-1251', 'ignore').replace(
                        ' class="trivia"', '')

        # movies
        from kinopoisk.person import Role
        self.content = html.fromstring(self.content)
        for element in self.extract('movies'):
            type = [t.get('data-work-type') for t in element.iterancestors()][0]
            self.instance.career.setdefault(type, [])
            self.instance.career[type].append(Role.get_parsed('role_link', element))

        self.instance.set_source('main_page')


class PersonPhotosPage(KinopoiskImagesPage):
    """
    Parser of person photos page
    """
    url = '/name/{id}/photos/'
    field_name = 'photos'
