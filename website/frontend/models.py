import subprocess
import os
import json

from datetime import datetime
from urlparse import urlparse

from django.db import models

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(THIS_DIR))
GIT_DIR = ROOT_DIR+'/articles/'

GIT_PROGRAM = 'git'

ancient = datetime(1901, 1, 1)

# Create your models here.
class Article(models.Model):
    class Meta:
        db_table = 'Articles'

    url = models.CharField(max_length=255, blank=False, unique=True,
                           db_index=True)
    initial_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(default=ancient)
    last_check = models.DateTimeField(default=ancient)
    git_dir = models.CharField(max_length=255, blank=False, default='old')

    def __unicode__(self):
        return "%s" % (self.url)

    @property
    def full_git_dir(self):
        return GIT_DIR + self.git_dir

    def filename(self):
        parsed = urlparse(self.url)
        path = parsed.path.rstrip('/')

        # path doesn't have any trailing slash, and whatever was left after
        # rstrip(), is a reasonably valid path
        ret = parsed.hostname + path + '/index.html'

        return ret

    def publication(self):
        parsed = urlparse(self.url)
        return parsed.hostname

    def versions(self):
        return self.version_set.filter(boring=False).order_by('date')

    def latest_version(self):
        return self.versions().latest()

    def first_version(self):
        return self.versions()[0]

    def minutes_since_update(self):
        delta = datetime.now() - max(self.last_update, self.initial_date)
        return delta.seconds // 60 + 24*60*delta.days

    def minutes_since_check(self):
        delta = datetime.now() - self.last_check
        return delta.seconds // 60 + 24*60*delta.days

class Version(models.Model):
    class Meta:
        db_table = 'version'
        get_latest_by = 'date'

    article = models.ForeignKey('Article', null=False)
    v = models.CharField(max_length=255, blank=False, unique=True)
    title = models.CharField(max_length=255, blank=False)
    byline = models.CharField(max_length=255,blank=False)
    date = models.DateTimeField(blank=False)
    boring = models.BooleanField(blank=False, default=False)
    diff_json = models.CharField(max_length=255, null=True)

    def __unicode__(self):
        return "%s for %s" % (self.v, self.article)

    def text(self):
        version = self.v + ':' + self.article.filename()
        try:
            return subprocess.check_output([GIT_PROGRAM, 'show', version],
                                           cwd=self.article.full_git_dir)
        except subprocess.CalledProcessError as e:
            return None

    def get_diff_info(self):
        if self.diff_json is None:
            return {}
        return json.loads(self.diff_json)
    def set_diff_info(self, val=None):
        if val is None:
            self.diff_json = None
        else:
            self.diff_json = json.dumps(val)
    diff_info = property(get_diff_info, set_diff_info)

class StandaloneArticle(models.Model):
    url = models.CharField(max_length=255, blank=False, unique=True,
                           db_index=True)
    added_by = models.CharField(max_length=255, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % (self.url)
