# -*- coding: utf-8 -*-
from kinopoisk.utils import KinopoiskPage
import re

class PersonLink(KinopoiskPage):
    '''
    Parser person info from links
    '''
    def parse(self, instance, content):

        link = re.compile(r'<p class="name"><a href="http://www.kinopoisk.ru/level/4/people/(\d+)/[^"]*">(.+?)</a>').findall(content)
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
    '''
    Parser of main person page
    '''
    url = '/level/4/people/%d/'

    def parse(self, instance, content):

        id = re.compile(r"pageUrl:'http://www.kinopoisk.ru/level/4/people/(\d+)/vk/3/'").findall(content)
        if id:
            instance.id = self.prepare_int(id[0])

        name = re.compile(r'<h1 style="padding:0px;margin:0px" class="moviename-big">(.+?)</h1>').findall(content)
        if name:
            instance.name = self.prepare_str(name[0])

        name_original = re.compile(r'<span style="font-size:13px;color:#666">(.+?)</span>').findall(content)
        if name_original:
            instance.name_original = self.prepare_str(name_original[0])

        content_info = content[content.find(u'<!-- инфа об актере -->'):content.find(u'<!-- /инфа об актере -->')]
        content_info = re.compile(r'<tr\s*>\s*<td class="type">(.+?)</td>\s*<td[^>]*>(.+?)</td>\s*</tr>').findall(content_info)
        for name, value in content_info:
            if name == u'дата рождения':
                year_birth = re.compile(r'<a href="/level/10/m_act%5Bbirthday%5D%5Byear%5D/\d{4}/">(\d{4})</a>').findall(value)
#                year_birth = re.compile(r'<a href="/level/10/m_act\[birthday\]\[year\]/\d{4}/">(\d{4})</a>').findall(value)
                if year_birth:
                    instance.year_birth = self.prepare_int(year_birth[0])

        instance.set_source('main_page')