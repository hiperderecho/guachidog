from baseparser import BaseParser, logger
from BeautifulSoup import BeautifulSoup

from django.utils import timezone
from website.frontend import models

class StandaloneParser(BaseParser):
    # These are populated from the database
    domains = ['standalone']
    feeder_pages = ['']

    @classmethod
    def feed_urls(cls):
        db_objs = models.StandaloneArticle.objects.all()
        return [obj.url for obj in db_objs]

    def _parse(self, html):
        self.meta = ''
        self.title = self.url
        self.date = timezone.now().strftime('%Y-%m-%d %H:%m:%S')
        self.byline = ''
        self.body = unicode(html, 'utf-8')
