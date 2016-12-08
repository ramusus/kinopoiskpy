# -*- coding: utf-8 -*-
"""
Sources for Person
"""
from __future__ import unicode_literals

import re

from builtins import str

from ..utils import KinopoiskPage, KinopoiskImagesPage, get_request


class PersonLink(KinopoiskPage):
    """
    Parser person info from links
    """

    def parse(self, instance, content):
        link = re.compile(r'<p class="name"><a[^>]+href="/name/(\d+)/[^"]*">(.+?)</a>').findall(content)
        if link:
            instance.id = self.prepare_int(link[0][0])
            instance.name = self.prepare_str(link[0][1])

        year = re.compile(r'<span class="year">(\d{4})</span>').findall(content)
        if year:
            instance.year_birth = self.prepare_int(year[0])

        otitle = re.compile(r'<span class="gray">(.*?)</span>').findall(content)
        if otitle:
            instance.name_original = self.prepare_str(otitle[0])

        instance.set_source('link')


class PersonMainPage(KinopoiskPage):
    """
    Parser of main person page
    """
    url = '/name/%d/'

    def parse(self, instance, content):

        person_id = re.compile(r"<link rel=\"canonical\" href=\"https?://www.kinopoisk.ru/name/(\d+)/\" />").findall(
            content)
        if person_id:
            instance.id = self.prepare_int(person_id[0])

        name = re.compile(r'<h1 class="moviename-big" itemprop="name">(.+?)</h1>').findall(content)
        if name:
            instance.name = self.prepare_str(name[0])

        name_original = re.compile(r'<span itemprop="alternateName">([A-Z]\'?[- a-zA-Z]+)</span>').findall(content)
        if name_original:
            instance.name_original = self.prepare_str(name_original[0])

        content_info = re.compile(r'<tr\s*>\s*<td class="type">(.+?)</td>\s*<td[^>]*>(.+?)</td>\s*</tr>').findall(
            content)
        for name, value in content_info:
            if str(name) == 'дата рождения':
                year_birth = re.compile(r'<a href="/lists/m_act%5Bbirthday%5D%5Byear%5D/\d{4}/">(\d{4})</a>').findall(
                    value)
                if year_birth:
                    instance.year_birth = self.prepare_int(year_birth[0])

        if instance.id:
            response = get_request(instance.get_url('info'))
            response.connection.close()
            if response.content:
                instance.information = response.content.decode('windows-1251', 'ignore').replace(' class="trivia"', '')

        instance.set_source('main_page')


class PersonPhotosPage(KinopoiskImagesPage):
    """
    Parser of person photos page
    """
    url = '/name/%d/photos/'
    field_name = 'photos'
