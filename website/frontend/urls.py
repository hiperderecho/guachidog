from django.conf.urls import url

urlpatterns = [
  url(r'^diff/(?P<vid1>\d+)/(?P<vid2>\d+)/(?P<urlarg>.*)$', 'frontend.views.diffview', name='diffview'),

  # Feed URLs
  url(r'^feed/(.*)$', 'frontend.views.feed', name='feed'),
  url(r'^feed/article-history/(.*)$', 'frontend.views.article_history_feed', name='article_history_feed'),

  url(r'^article-history/$', 'frontend.views.article_history', name='article_history'),
  url(r'^article-history/(?P<urlarg>.*)$', 'frontend.views.article_history', name='article_history'),

  url(r'^json/(?P<vid>\d+)/?$', 'frontend.views.json_view'),

  url(r'^$', 'frontend.views.browse', name='root'),
]
