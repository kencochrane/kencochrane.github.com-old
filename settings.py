#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Ken Cochrane'
DISQUS_SITENAME = 'kencochrane'
GITHUB_URL = 'https://github.com/kencochrane/kencochrane.github.com'
GITHUB_ACTIVITY_FEED = 'https://github.com/kencochrane.atom'
GOOGLE_ANALYTICS='UA-67696-11'
CLICKY_SITE_ID='66415850'
SITEURL = 'http://kencochrane.net'
FEED_DOMAIN = SITEURL
SITENAME = 'KenCochrane.net'
SOCIAL = (('twitter', 'http://twitter.com/kencochrane'),
          ('github', 'https://github.com/kencochrane'),)
TAG_FEED_ATOM = 'feeds/%s.atom.xml'
TAG_FEED_RSS = 'rss/%s.rss'
FEED_ALL_RSS = 'rss/all.rss'
THEME='kencochrane/ken_theme'
TWITTER_USERNAME = 'KenCochrane'
PLUGIN_PATH = '/Users/ken/projects/github/pelican-plugins'
# PLUGINS = ['gravatar',
#            'github_activity',
#            'related_posts',
#            'html_rst_directive']
PLUGINS = ['pelican.plugins.gravatar',
           'pelican.plugins.github_activity',
           'pelican.plugins.related_posts',
           'pelican.plugins.html_rst_directive']
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{slug}/index.html'
PAGE_URL = '{slug}/index.html'
PAGE_SAVE_AS = '{slug}/index.html'
DISPLAY_PAGES_ON_MENU = True
MARKUP = (('rst','html'))
TIMEZONE = 'America/New_York'
DEFAULT_LANG = 'en'
DEFAULT_PAGINATION = 10
ARTICLE_DIR = ('content')
ARTICLE_EXCLUDES = (('kencochrane','pages'))
USE_FOLDER_AS_CATEGORY = False
THEME_STATIC_PATHS = (['static'])
SUMMARY_MAX_LENGTH = 100