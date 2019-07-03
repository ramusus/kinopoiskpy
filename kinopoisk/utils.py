# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import six
import unicodedata

from builtins import str

from .request import Request


class Manager(object):
    kinopoisk_object = None
    search_url = None

    def __init__(self):
        self.request = Request()

    def search(self, query):
        url, params = self.get_url_with_params(query)
        response = self.request.get(url, params=params)
        content = response.content.decode('utf-8')
        self.request.raise_for_errors(content)
        # request is redirected to main page of object
        if len(response.history) and ('/film/' in response.url or '/name/' in response.url):
            instance = self.kinopoisk_object()
            instance.get_source_instance(
                'main_page', instance=instance, content=content, request=self.request).parse()
            return [instance]
        else:
            # <h2 class="textorangebig" style="font:100 18px">К сожалению, сервер недоступен...</h2>
            if content.find('<h2 class="textorangebig" style="font:100 18px">') != -1:
                return []
            content_results = content[content.find('<div class="search_results">'):content.find(
                '<div style="height: 40px"></div>')]
            if content_results:
                from bs4 import BeautifulSoup  # import here for successful installing via pip
                soup_results = BeautifulSoup(content_results, 'html.parser')
                # <div class="element width_2">
                results = soup_results.findAll('div', attrs={'class': re.compile('element')})
                if not results:
                    raise ValueError('No objects found in search results by request "%s"' % response.url)
                instances = []
                for result in results:
                    instance = self.kinopoisk_object.get_parsed('link', str(result))
                    if instance.id:
                        instances += [instance]
                return instances

            raise ValueError('Unknown html layout found by request "%s"' % response.url)

    def get_url_with_params(self, query):
        return 'http://www.kinopoisk.ru/index.php', {'kp_query': query}

    def get_first(self, query):
        self.search(query)


# htmlf=html[html.find('<!-- результаты поиска -->'):html.find('<!-- /результаты поиска -->')]
#        if htmlf<>"":
#            htmlf = htmlf[htmlf.find('Скорее всего вы ищете'):htmlf.find('</a>')]
#            htmlf=re.compile(r'<a class="all" href="(.+?)">').findall(htmlf)
#            try:
#                html = UrlRequest("http://www.kinopoisk.ru"+htmlf[0]).read()
#            except urllib2.URLError, why:
#                return None
#                exit


class KinopoiskObject(object):
    id = None
    objects = None

    _urls = {}
    _sources = []
    _source_classes = {}

    def __init__(self, id=None, **kwargs):
        if id:
            self.id = id
        self.set_defaults()
        self.__dict__.update(kwargs)

    def set_defaults(self):
        pass

    def parse(self, name, content):
        """Parse using registered parser `name` and content"""
        self.get_source_instance(name, instance=self, content=content).parse()

    def get_content(self, name):
        """Populate instance with data from source `name`"""
        self.get_source_instance(name, instance=self).get()

    @classmethod
    def get_parsed(cls, name, content):
        """Initialize, parse and return instance"""
        instance = cls()
        instance.parse(name, content)
        return instance

    def register_source(self, name, class_name):
        try:
            self.set_url(name, class_name.url)
        except AttributeError:
            pass
        self.set_source(name)
        self._source_classes[name] = class_name

    def set_url(self, name, url):
        self._urls[name] = url

    def get_url(self, name, postfix='', **kwargs):
        url = self._urls.get(name)
        if not url:
            raise ValueError('There is no urlpage with name "%s"' % name)
        if not self.id:
            raise ValueError('ID of object is empty')
        kwargs['id'] = self.id
        return ('http://www.kinopoisk.ru' + url).format(**kwargs) + postfix

    def set_source(self, name):
        if name not in self._sources:
            self._sources += [name]

    def get_source_instance(self, name, **kwargs):
        class_name = self._source_classes.get(name)
        if not class_name:
            raise ValueError('There is no source with name "%s"' % name)
        instance = class_name(name, **kwargs)
        return instance


class KinopoiskImage(KinopoiskObject):
    def __init__(self, id=None):
        super(KinopoiskImage, self).__init__(id)
        self.set_url('picture', '/picture/{id}/')

    def get_url(self, name='picture', postfix='', **kwargs):
        return super(KinopoiskImage, self).get_url(name, postfix=postfix, **kwargs)


class KinopoiskPage(object):
    content = None

    def __init__(self, source_name, instance, content=None, request=None):
        self.request = request or Request()
        self.source_name = source_name
        self.instance = instance
        if content is not None:
            self.content = content

    @property
    def element(self):
        return self.content

    @property
    def xpath(self):
        raise NotImplementedError()

    def extract(self, name, to_str=False, to_int=False, to_float=False):
        if name in self.xpath:
            xpath = self.xpath[name]
            elements = self.element.xpath(xpath)
            if xpath[-7:] == '/text()' or '/@' in xpath:
                value = ' '.join(elements) if elements else ''
            else:
                value = elements
            if to_str:
                value = self.prepare_str(value)
            if to_int:
                value = self.prepare_int(value) if value else None
            if to_float:
                value = float(value) if value else None
            return value
        else:
            raise ValueError("Xpath element with name `{}` is not configured".format(name))

    def prepare_str(self, value):
        if six.PY2:
            # BS4 specific replacements
            value = re.compile(' ').sub(' ', value)
            value = re.compile('').sub('—', value)
            # General replacements
            value = re.compile(r", \.\.\.").sub("", value)
        else:
            value = unicodedata.normalize("NFKC", value)
        value = restore_characters(value)
        return value.strip()

    def prepare_int(self, value):
        value = self.prepare_str(value)
        value = value.replace(' ', '')
        value = int(value)
        return value

    def prepare_date(self, value):
        value = self.prepare_str(value).strip()
        if not value:
            return None
        months = ["января", "февраля", "марта", "апреля", "мая", "июня",
                  "июля", "августа", "сентября", "октября", "ноября", "декабря"]
        for i, month in enumerate(months, start=1):
            if month in value:
                value = value.replace(month, '%02d' % i)
                break
        value = value.replace('\xa0', '-')
        from dateutil import parser
        return parser.parse(value, dayfirst=True).date()

    def prepare_profit(self, value):
        profit = value
        if '=' in profit:
            profit = profit[profit.index('=') + 1:]

        # Remove all whitespace characters
        profit = ''.join(profit.split())

        # Remove currency symbol to cast budget to int
        profit = profit[1:]
        return self.prepare_int(profit)

    def find_profit(self, td):
        for tag in [td.find('a'), td.find('div')]:
            if tag:
                for value in tag.contents:
                    if '$' in value:
                        return self.prepare_profit(value)

    def cut_from_to(self, content, after, before):
        start = content.find(after)
        end = content.find(before)
        if start != -1 and end != -1:
            content = content[start:end]
        return content

    def get(self):
        if self.instance.id:
            self.content = self.request.get_content(self.instance.get_url(self.source_name))
            self.parse()
            return
        raise NotImplementedError('This method must be implemented in subclass')

    def parse(self):
        raise NotImplementedError('You must implement KinopoiskPage.parse() method')

    def split_triple_dots(self, role):
        role = role.strip().split(' ... ')
        # if no original title and role starts with '... '
        if len(role) == 1 and role[0][:3] == '...':
            role = role[0].strip().split('... ')
        return role


class KinopoiskImagesPage(KinopoiskPage):
    """
    Parser of kinopoisk images page
    """
    field_name = None

    def get(self, page=1):
        content = self.request.get_content(self.instance.get_url(self.source_name, postfix='page/{}/'.format(page)))

        # header with sign 'No posters'
        if re.findall(r'<h1 class="main_title">', content):
            return False

        content = content[content.find('<div style="padding-left: 20px">'):content.find('        </td></tr>')]

        from bs4 import BeautifulSoup
        soup_content = BeautifulSoup(content, 'html.parser')
        table = soup_content.findAll('table', attrs={'class': re.compile('^fotos')})
        if table:
            self.content = str(table[0])
            self.parse()
            # may be there is more pages?
            if len(getattr(self.instance, self.field_name)) % 21 == 0:
                try:
                    self.get(page + 1)
                except ValueError:
                    return
        else:
            raise ValueError('Parse error. Do not found posters for movie %s' % (self.instance.get_url('posters')))

    def parse(self,):
        urls = getattr(self.instance, self.field_name, [])

        from bs4 import BeautifulSoup
        links = BeautifulSoup(self.content, 'html.parser').findAll('a')
        for link in links:

            img_id = re.compile(r'/picture/(\d+)/').findall(link['href'])
            picture = KinopoiskImage(int(img_id[0]))

            content = self.request.get_content(picture.get_url())
            img = BeautifulSoup(content, 'html.parser').find('img', attrs={'id': 'image'})
            if img:
                img_url = img['src']
                if img_url not in urls:
                    urls.append(img_url)

        setattr(self.instance, self.field_name, urls)
        self.instance.set_source(self.source_name)


def restore_characters(s):
    """Replace C1 control characters in the Unicode string s by the
    characters at the corresponding code points in Windows-1252,
    where possible.
    """
    def restore(match):
        try:
            return bytes([ord(match.group(0))]).decode('windows-1251')
        except UnicodeDecodeError:
            # No character at the corresponding code point: remove it.
            return ''
    return re.sub(r'[\u0080-\u0099]', restore, s)
