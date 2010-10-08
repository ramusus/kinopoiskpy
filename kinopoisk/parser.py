# -*- coding: utf-8 -*-
import urllib, urllib2
from urlparse import urlparse
import sys

class UrlRequest(object):

    url = None
    params = None

    final_url = None

    _headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.9.1.8) Gecko/20100214 Linux Mint/8 (Helena) Firefox/3.5.8',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru,en-us;q=0.7,en;q=0.3',
        'Accept-Encoding': 'deflate',
        'Accept-Charset': 'windows-1251,utf-8;q=0.7,*;q=0.7',
        'Keep-Alive': '300',
        'Connection': 'keep-alive',
        'Referer': 'http://www.kinopoisk.ru/',
        'Cookie': 'users_info[check_sh_bool]=none; search_last_date=2010-02-19; search_last_month=2010-02;                                        PHPSESSID=b6df76a958983da150476d9cfa0aab18',
    }

    @property
    def is_redirected(self):
        return urlparse(self.url).path != urlparse(self.final_url).path

    def __init__(self, url, params=None):
        self.url = url
        if isinstance(params, dict):
            self.params = dict([(key, unicode(val).encode('windows-1251')) for key, val in params.items()])

    def read(self):
        response = urllib2.urlopen(self._get_request())
        self.final_url = response.geturl()
        return response.read().decode('windows-1251')

    def _get_url(self):
        url = self.url
        if self.params:
            url += '?' + urllib.urlencode(self.params)
        return url

    def _get_request(self):
        return urllib2.Request(url=self._get_url(), headers = self._headers)