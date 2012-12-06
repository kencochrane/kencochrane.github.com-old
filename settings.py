#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Ken Cochrane'
DISQUS_SITENAME = 'kencochrane'
GITHUB_URL = 'https://github.com/kencochrane/kencochrane.github.com'
GITHUB_ACTIVITY_FEED = 'https://github.com/kencochrane.atom'
GOOGLE_ANALYTICS='UA-67696-11'
CLICKY_SITE_ID='66415850'
#CSS_FILE = "wide.css"
SITEURL = 'http://kencochrane.net'
SITENAME = 'KenCochrane.net'
SOCIAL = (('twitter', 'http://twitter.com/kencochrane'),
          ('github', 'https://github.com/kencochrane'),)
TAG_FEED_ATOM = 'feeds/%s.atom.xml'
TAG_FEED_RSS = 'rss/%s.rss'
FEED_ALL_RSS = 'rss/all.rss'
THEME='notmyidea'
TWITTER_USERNAME = 'KenCochrane'
PLUGINS = ['pelican.plugins.gravatar',
           'pelican.plugins.github_activity',
           'pelican.plugins.related_posts',
           'pelican.plugins.html_rst_directive']
ARTICLE_URL = 'blog/{date:%Y}/{date:%b}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%b}/{date:%d}/{slug}/index.html'
PAGE_URL = '{slug}/index.html'
PAGE_SAVE_AS = '{slug}/index.html'
DISPLAY_PAGES_ON_MENU = True
MARKUP = (('rst',))
TIMEZONE = 'America/New_York'
DEFAULT_LANG = 'en'
DEFAULT_PAGINATION = 10