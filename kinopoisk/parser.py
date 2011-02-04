# -*- coding: utf-8 -*-
import urllib2
import urllib
import urlparse
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
        return urlparse.urlparse(self.url).path != urlparse.urlparse(self.final_url).path

    def __init__(self, url, params=None):
        self.url = url
        if isinstance(params, dict):
            self.params = params

    def read(self):
        response = urllib2.urlopen(self._get_request())
        self.final_url = response.geturl()
        return response.read().decode('windows-1251', 'ignore')

    def _get_url(self):
        url = self.url
        if self.params:
            url += '?' + '&'.join(['%s=%s' % (key, val) for key, val in self.params.items()])
        url = url_fix(url)
        return url

    def _get_request(self):
        return urllib2.Request(url=self._get_url(), headers = self._headers)

def url_fix(s, charset='utf-8'):
    """Sometimes you get an URL by a user that just isn't a real
    URL because it contains unsafe characters like ' ' and so on.  This
    function can fix some of the problems in a similar way browsers
    handle data entered by the user:

    >>> url_fix(u'http://de.wikipedia.org/wiki/Elf (Begriffsklärung)')
    'http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29'

    :param charset: The target charset for the URL if the url was
                    given as unicode string.
    """
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))