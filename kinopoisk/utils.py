# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from builtins import str


def get_request(url, params=None):
    import requests
    return requests.get(url, params=params, headers={
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.9.1.8) Gecko/20100214 Linux Mint/8 (Helena) Firefox/'
                      '3.5.8',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru,en-us;q=0.7,en;q=0.3',
        'Accept-Encoding': 'deflate',
        'Accept-Charset': 'windows-1251,utf-8;q=0.7,*;q=0.7',
        'Keep-Alive': '300',
        'Connection': 'keep-alive',
        'Referer': 'http://www.kinopoisk.ru/',
        'Cookie': 'users_info[check_sh_bool]=none; search_last_date=2010-02-19; search_last_month=2010-02;'
                  '                                        PHPSESSID=b6df76a958983da150476d9cfa0aab18',
    })


class Manager(object):
    kinopoisk_object = None
    search_url = None

    def search(self, query):
        url, params = self.get_url_with_params(query)
        response = get_request(url, params=params)
        response.connection.close()
        content = response.content.decode('windows-1251', 'ignore')
        # request is redirected to main page of object
        if len(response.history) and ('/film/' in response.url or '/name/' in response.url):
            instance = self.kinopoisk_object()
            instance.parse('main_page', content)
            return [instance]
        else:
            # <h2 class="textorangebig" style="font:100 18px">К сожалению, сервер недоступен...</h2>
            if content.find('<h2 class="textorangebig" style="font:100 18px">') != -1:
                return []
            content_results = content[content.find('<div class="search_results">'):content.find(
                '<div style="height: 40px"></div>')]
            if content_results:
                from bs4 import BeautifulSoup  # import here for successful installing via pip
                soup_results = BeautifulSoup(content_results, 'lxml')
                # <div class="element width_2">
                results = soup_results.findAll('div', attrs={'class': re.compile('element')})
                if not results:
                    raise ValueError('No objects found in search results by request "%s"' % response.url)
                instances = []
                for result in results:
                    instance = self.kinopoisk_object()
                    instance.parse('link', str(result))
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
        self.get_source_instance(name).parse(self, content)

    def get_content(self, name):
        self.get_source_instance(name).get(self)

    def register_source(self, name, class_name):
        try:
            self.set_url(name, class_name.url)
        except:
            pass
        self.set_source(name)
        self._source_classes[name] = class_name

    def set_url(self, name, url):
        self._urls[name] = url

    def get_url(self, name, postfix=''):
        url = self._urls.get(name)
        if not url:
            raise ValueError('There is no urlpage with name "%s"' % name)
        if not self.id:
            raise ValueError('ID of object is empty')
        return 'http://www.kinopoisk.ru' + url % self.id + postfix

    def set_source(self, name):
        if name not in self._sources:
            self._sources += [name]

    def get_source_instance(self, name):
        class_name = self._source_classes.get(name)
        if not class_name:
            raise ValueError('There is no source with name "%s"' % name)
        instance = class_name()
        instance.content_name = name
        return instance


class KinopoiskImage(KinopoiskObject):
    def __init__(self, id=None):
        super(KinopoiskImage, self).__init__(id)
        self.set_url('picture', '/picture/%d/')

    def get_url(self, name='picture', postfix=''):
        return super(KinopoiskImage, self).get_url(name, postfix)


class KinopoiskPage(object):
    content_name = None

    def prepare_str(self, value):
        # BS4 specific replacements
        value = re.compile(' ').sub(' ', value)
        value = re.compile('').sub('—', value)
        # General replacements
        value = re.compile(r", \.\.\.").sub("", value)
        return value.strip()

    def prepare_int(self, value):
        value = self.prepare_str(value)
        value = int(value)
        return value

    def prepare_date(self, value):
        value = self.prepare_str(value).strip()
        if not value:
            return None
        months = [u"января", u"февраля", u"марта", u"апреля", u"мая", u"июня",
                  u"июля", u"августа", u"сентября", u"октября", u"ноября", u"декабря"]
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

    def get(self, instance):
        if instance.id:
            response = get_request(instance.get_url(self.content_name))
            response.connection.close()
            content = response.content.decode('windows-1251', 'ignore')
            # content = content[content.find('<div style="padding-left: 20px">'):content.find('        </td></tr>')]
            self.parse(instance, content)
            return
        raise NotImplementedError('This method must be implemented in subclass')

    def parse(self, instance, content):
        raise NotImplementedError('You must implement KinopoiskPage.parse() method')


class KinopoiskImagesPage(KinopoiskPage):
    """
    Parser of kinopoisk images page
    """
    field_name = None

    def get(self, instance, page=1):
        response = get_request(instance.get_url(self.content_name, postfix='page/%d/' % page))
        response.connection.close()
        content = response.content.decode('windows-1251', 'ignore')

        # header with sign 'No posters'
        if re.findall(r'<h1 class="main_title">', content):
            return False

        content = content[content.find('<div style="padding-left: 20px">'):content.find('        </td></tr>')]

        from bs4 import BeautifulSoup
        soup_content = BeautifulSoup(content, 'lxml')
        table = soup_content.findAll('table', attrs={'class': re.compile('^fotos')})
        if table:
            self.parse(instance, str(table[0]))
            # may be there is more pages?
            if len(getattr(instance, self.field_name)) % 21 == 0:
                try:
                    self.get(instance, page + 1)
                except ValueError:
                    return
        else:
            raise ValueError('Parse error. Do not found posters for movie %s' % (instance.get_url('posters')))

    def parse(self, instance, content):
        urls = getattr(instance, self.field_name, [])

        from bs4 import BeautifulSoup
        links = BeautifulSoup(content, 'lxml').findAll('a')
        for link in links:

            img_id = re.compile(r'/picture/(\d+)/').findall(link['href'])
            picture = KinopoiskImage(int(img_id[0]))

            response = get_request(picture.get_url())
            response.connection.close()
            content = response.content.decode('windows-1251', 'ignore')
            img = BeautifulSoup(content, 'lxml').find('img', attrs={'id': 'image'})
            if img:
                img_url = img['src']
                if img_url not in urls:
                    urls.append(img_url)

        setattr(instance, self.field_name, urls)
        instance.set_source(self.content_name)
