#!/usr/bin/env python
# -*- coding: utf-8 -*- #

DEFAULT_LANG = 'en'
# Blogroll
# LINKS =  (('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
#           ('Python.org', 'http://python.org'),
#           ('Jinja2', 'http://jinja.pocoo.org'),
#           ('You can modify those links in your config file', '#'),)

DEFAULT_PAGINATION = 10

AUTHOR = 'Ken Cochrane'
DISQUS_SITENAME = 'kencochrane'
GITHUB_URL = 'https://github.com/kencochrane'
GITHUB_ACTIVITY_FEED = 'https://github.com/kencochrane.atom'
GOOGLE_ANALYTICS='UA-67696-11'
CLICKY_SITE_ID='66415850'
SITEURL = 'http://kencochrane.net'
SITENAME = 'KenCochrane.net'
SOCIAL = (('twitter', 'http://twitter.com/kencochrane'),
          ('github', 'https://github.com/kencochrane'),)
#TAG_FEED_ATOM = 'feeds/%s.atom.xml'
THEME='notmyidea' #THEME='bootstrap'
TWITTER_USERNAME = 'KenCochrane'
PLUGINS = ['pelican.plugins.gravatar',
           'pelican.plugins.github_activity',
           'pelican.plugins.related_posts',
           'pelican.plugins.html_rst_directive']
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{slug}/index.html'
PAGE_URL = '{slug}/index.html'
PAGE_SAVE_AS = '{slug}/index.html'
DISPLAY_PAGES_ON_MENU = True
MARKUP = (('rst', 'html'))

TIMEZONE = 'America/New_York'
#DIRECT_TEMPLATES = (('index', 'tags', 'categories', 'archives'))
#CSS_FILE = "wide.css"
