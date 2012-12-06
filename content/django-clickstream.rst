
:date: 2011-08-12 10:48:29
:tags: 
:category: blog
:slug: django-clickstream
:author: Ken Cochrane
:title: django-clickstream


Track a visitors movements across your site.

Possible uses:

* See what they were doing before they got an error.

* Use it for analytics and usability testing to see how people are moving around your site, and where you are losing people.


Inspired by OpenSymphony's Java project of the same name. http://code.google.com/p/clickstream/ 

Requirements
------------
* Django 1.1 or newer
* Django sessions need to be enabled
* Django south 0.7 or newer for migrations

--------
Settings
--------

Custom Settings
===============

Add the following properties to your settings file if you want to override the default settings.


CLICKSTREAM_IGNORE_PATHS
========================

Default = ()

Takes a list of regular expressions for paths that you want to ignore if it is picked up by these clicks won't be tracked.

CLICKSTREAM_IGNORE_PATHS = ('^/private/', '^/dont-track-me/', 'super-secret.txt')

CLICKSTREAM_IGNORE_ANONYMOUS
============================

Default = False

If you only want to track people that are logged in, change to True

CLICKSTREAM_IGNORE_ANONYMOUS = False


CLICKSTREAM_IGNORE_IP
=====================
Default = ()

A list of IP's that you don't want to track

CLICKSTREAM_IGNORE_IP = ('127.0.0.1', '10.10.10.10, '8.8.8.8')

Middleware 
==========
Add 'clickstream.middleware.ClickStreamMiddleware' to your MIDDLEWARE_CLASSES settings 
it needs to be after 'django.contrib.sessions.middleware.SessionMiddleware' in the list.

App
===

Add clickstream to INSTALLED_APPS


Sync Tables + Migrate
=====================

Run './manage.py syncdb' to load up the tables in your database.

Run './manage.py migrate' to run the south migrations


