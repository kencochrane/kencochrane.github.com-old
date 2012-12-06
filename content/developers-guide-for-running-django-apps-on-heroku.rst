
:date: 2011-11-30 10:00:00
:tags: django,python,heroku,hosting,deployment,paas
:category: blog
:slug: developers-guide-for-running-django-apps-on-heroku
:author: Ken Cochrane
:title: Developers guide to Running Django Applications on Heroku

`Heroku <http://Heroku.com>`_ the platform as a service (PAAS) company, very popular in the Ruby on Rails community, has now started opening up their platform to languages besides Ruby. They now offer support for Python, Java, Clojure, Node.js, and Scala on their new Cedar stack. Heroku's Cedar stack is still in beta, but that shouldn't stop you from trying it out, and that is just what I'm going to do. 

6 months ago I wrote a series of blog posts that reviewed all of the cool new django hosting services that were popping up. My goal was to look at them all, and compare them to find out what they had to offer, and to see if I could use them on my future projects. I'm going to review Heroku using the same process that I used to review those other services, so that I can we can compare apples to apples. 

For those of you who are not familiar with my other blog posts, feel free to check them out now `ep.io <http://kencochrane.net/blog/2011/04/my-experiences-with-epio/>`_, `apphosted.com <http://kencochrane.net/blog/2011/05/apphosted-com-django-hosting-review/>`_, `gondor.io <http://kencochrane.net/blog/2011/04/my-day-gondorio/>`_, `dotcloud.com <http://kencochrane.net/blog/2011/04/deploying-my-django-application-to-dotcloud/>`_, `DjangoZoom.com <http://DjangoZoom.com>`_, `Django hosting roundup <http://kencochrane.net/blog/2011/06/django-hosting-roundup-who-wins/>`_.

For those of you that are lazy, I'll sum it up pretty quickly. What I'm trying to do is pretty simple, I sign up for the service, and just looking at the documentation available, can I get my blog application up and running, and what did I have to do, in order for it to work. I'll describe each step along the way, as a helpful guide for others who might be trying to do the same with their application. If I come across an error, I will tell you what the error was, and how I fixed it, so that if you get the same error, hopefully what I did to fix my problem, will also fix yours.

Heroku Django Documentation
===========================

Before you start using any new platform, you should take the time to read the documentation. I know it doesn't sound like fun,but trust me, it will save you a lot of pain and frustration later on. Here are some links that I found helpful. 

- **Quickstart guide**: http://devcenter.heroku.com/articles/quickstart
- **Python articles**: http://devcenter.heroku.com/articles/python
- **Django article**: http://devcenter.heroku.com/articles/django
- **Dev Center**: http://devcenter.heroku.com/


Prerequisites
=============
- Heroku account
- Heroku command line client 
- Python 2.7, virtualenv, pip, git
- Must use pip to manage dependencies with a requirements.txt file


Signing up for Heroku
=====================

Signing up was as simple as can be, all I needed to do was follow this link: https://api.heroku.com/signup and fill out my email address. Go into my email and click on the link they sent, which took me to a page that had me pick my password, and I was done. The whole process took less then 1 minute. Can't beat that.

Verifying you Heroku account
============================

When you sign up for an account, you have limited access to some features (add-ons, etc.) until you verify your account. Verifing your account is easy all you have to do is enter your credit card information. This proves to them you are real, and also allows you to use some of the paid features. I recommend that you verify your account so that you can get access to some of the nice free add-ons that are available.


Installing the heroku command line client
=========================================

I'm using a mac so I'm going to install the following version of the heroku command line client (toolbelt). 
http://toolbelt.herokuapp.com/osx/download

1. Click on link, download the file.
2. Find the file that was downloaded (heroku-toolbelt.pkg) and double click it.
3. Follow prompts; enter password when prompted, and click close.

Test heroku command line client
===============================

1. Open terminial
2. Type "heroku version" you should see something like this "heroku-gem/2.14.0" if so, it worked. if not, you did something wrong.

Login to heroku from command line client
========================================

Logging into the client will try to find your ssh key, and upload it to heroku for pushing code later on. If you don't have a key it will prompt you to create one. If you have more then one it will ask you which one you want to use.

No key found example
--------------------

.. code-block:: bash

    $ heroku login
    Enter your Heroku credentials.
    Email: adam@example.comPassword: 
    Could not find an existing public key.
    Would you like to generate one? [Yn] 
    Generating new SSH public key. 
    Uploading ssh public key /Users/adam/.ssh/id_rsa.pub

Found more then one key example
-------------------------------

.. code-block:: bash

    $ heroku login
    Enter your Heroku credentials.
    Email: <my email>
    Password:
    Found the following SSH public keys:
    1) apphosted.key.pub
    2) id_rsa.pub
    Which would you like to use with your Heroku account? 2
    Uploading ssh public key /Users/ken/.ssh/id_rsa.pub

Getting your Django application ready
=====================================

Now that you have an account and the client installed, you are ready to get started. If you are starting from scratch I recommend following the steps in this tutorial. http://devcenter.heroku.com/articles/django . If you are like me and already have an application that you want to install on to Heroku, keep reading.

Since I already have a project, I'm going to tell you what I needed to do in order to get my blog application up and running on heroku. I followed the instructions from the heroku tutorial and went from there. Heroku depends on git, so I'm using a copy of my blog app that is hosted on github: https://github.com/kencochrane/kencochrane_blog_heroku

.. code-block:: bash

    $ cd /Users/ken/projects/github

    $ git clone https://kencochrane@github.com/kencochrane/kencochrane_blog_heroku.git kencochrane_heroku
    $ cd kencochrane_heroku

    # making a new virtual environment using virtualenvwrapper.
    $ mkvirtualenv --no-site-packages --distribute kencochrane_heroku 

It should automatically activate the environment for you. If it doesn't, run this command.

.. code-block:: bash

    $ workon kencochrane_heroku 

Now that I have my virtualenv, I need to install my requirements using pip.

.. code-block:: bash

    $ pip install -r requirements.txt

Creating django application on heroku
=====================================

Creating an application on heroku is easy, you just need to run the following command.

.. code-block:: bash

    $ heroku create --stack cedar
    Creating some-name-4741... done, stack is cedar
    http://some-name-4741.herokuapp.com/ | git@heroku.com:some-name-4741.git
    Git remote heroku added


Deploying django application to Heroku
======================================

Once you are ready you can deploy your django application to Heroku.

.. code-block:: bash

    $ git push heroku master

If everything went well, it should look something like this.

.. code-block:: bash
                                
    $ git push heroku master
    Counting objects: 209, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (176/176), done.
    Writing objects: 100% (209/209), 271.89 KiB, done.
    Total 209 (delta 28), reused 192 (delta 23)

    -----> Heroku receiving push
    -----> Python/Django app detected
    -----> Preparing virtualenv version 1.6.4
           New python executable in ./bin/python
           Installing setuptools............done.
           Installing pip...............done.
    -----> Django settings injection
           Injecting code into blog/settings.py to read from DATABASE_URL

    <removed a lot of output that doesn't need to be shown>

           Successfully installed South django-activitysync django-debug-toolbar django-disqus django-memcache-status django-tagging django-xmlrpc feedparser httplib2 oauth2 python-memcached python-twitter simplejson yolk docutils Pygments psycopg2 Django
           Cleaning up...
    -----> Discovering process types
           Procfile declares types         -> (none)
           Default types for Python/Django -> web
    -----> Compiled slug size is 10.3MB
    -----> Launching... done, v5
           http://some-name-4741.herokuapp.com deployed to Heroku


Deploying application to Heroku failed, now what?
=================================================

The very first time you push to master you will get something like this.

.. code-block:: bash

    $ git push heroku master

    The authenticity of host 'heroku.com (50.19.85.132)' can't be established.
    RSA key fingerprint is 8b:48:5e:67:0e:c9:16:47:32:f2:87:0c:1f:c8:60:ad.
    Are you sure you want to continue connecting (yes/no)? yes

This is normal, just type 'yes', and you will never be prompted for this again.

Django app must be in a package subdirectory
--------------------------------------------

If you django project isn't setup correctly, you will get an error like this.

.. code-block:: bash

    $ git push heroku master
    Counting objects: 199, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (167/167), done.
    Writing objects: 100% (199/199), 270.86 KiB, done.
    Total 199 (delta 26), reused 192 (delta 23)


    -----> Heroku receiving push
    -----> Python app detected
     !     Django app must be in a package subdirectory
     !     Heroku push rejected, failed to compile Python app


    To git@heroku.com:some-name-4741.git
     ! [remote rejected] master -> master (pre-receive hook declined)
    error: failed to push some refs to 'git@heroku.com:some-name-4741.git'


This failed, because django app must be in a package subdirectory.. So you need to change the way my django app is setup. Move all of the files under a django project directory except the .git directory and .gitignore and requirements.txt files. For an example of what this looks like, check out the project directory structure on my repo in github.


Heroku push rejected, no Cedar-supported app detected
-----------------------------------------------------

Another error you can get is this one. "Heroku push rejected, no Cedar-supported app detected"

.. code-block:: bash

    $ git push heroku master
    Counting objects: 204, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (171/171), done.
    Writing objects: 100% (204/204), 271.34 KiB, done.
    Total 204 (delta 27), reused 192 (delta 23)

    -----> Heroku receiving push
     !     Heroku push rejected, no Cedar-supported app detected

    To git@heroku.com:cold-summer-4741.git
     ! [remote rejected] master -> master (pre-receive hook declined)
    error: failed to push some refs to 'git@heroku.com:cold-summer-4741.git'

I had this error and I couldn't figure it out. After searching through all of the heroku python docs (all 2 of them), I didn't find anything, so I started doing some trial and error testing, and I finally figure out what was wrong. My django project directory was kencochrane_blog, and this had an underscore, and when I changed it to just kenblog (no more underscore), it worked. I couldn't find anything anywhere that said you can't use underscores for your django app name, so they might want to update their documentation, or possibly fix the bug. I'm not sure if this is by design or not, maybe someone can let me know.


Check Django application status on heroku
=========================================

Now that you have pushed your application out onto Heroku how do you know if it is actually running? The Heroku client has a command called ps, which will tell you what your processes are doing.

.. code-block:: bash

    $ heroku ps

    Process       State               Command
    ------------  ------------------  ------------------------------
    web.1         crashed for 2m      python kenblog/manage.py runserver 0...


My django application looks like it crashed. Most likely because I didn't setup the database yet, lets look at the logs to see what is causing the problems to be sure. 


Checking Django application logs on Heroku
==========================================

The Heroku client has a nifty logs command that you can use to view the last chunk of logs for your application. It will combine all of your logs into one view, so that you don't have to have more then one log process running. You can call it directly and get an output similar to the shell command 'tail' and you can all use the '--tail' option to follow the logs.

.. code-block:: bash

    $ heroku logs --tail
    2011-11-27T18:40:00+00:00 heroku[api]: Deploy 5f194d2 by kencochrane@2011-11-27T18:40:00+00:00 heroku[api]: Release v7 created by kencochrane@
    2011-11-27T18:40:00+00:00 heroku[web.1]: State changed from crashed to created
    2011-11-27T18:40:00+00:00 heroku[web.1]: State changed from created to starting
    2011-11-27T18:40:00+00:00 heroku[slugc]: Slug compilation finished
    2011-11-27T18:40:03+00:00 heroku[web.1]: Starting process with command `python kenblog/manage.py runserver 0.0.0.0:12033 --noreload`
    2011-11-27T18:40:04+00:00 app[web.1]: Unexpected error: (<type 'exceptions.NameError'>, NameError("name 'DATABASES' is not defined",), <traceback object at 0x1a7b128>)
    2011-11-27T18:40:05+00:00 app[web.1]: There is no South database module 'south.db.None' for your database. Please either choose a supported database, check for SOUTH_DATABASE_ADAPTER[S] settings, or remove South from INSTALLED_APPS.
    2011-11-27T18:40:06+00:00 heroku[web.1]: State changed from starting to crashed

Looks like it is an issue with the settings file. If you wanted to take a look at the settings file to see if we can find out what is wrong you can run the following command.

.. code-block:: bash

    # (your path will be different)
    $ heroku run cat kenblog/settings.py 

    <normal settings file stuff with the following added at the end.>

.. code-block:: python

    import os, sys, urlparse
    urlparse.uses_netloc.append('postgres')
    urlparse.uses_netloc.append('mysql')
    try:
        if os.environ.has_key('DATABASE_URL'):
            url = urlparse.urlparse(os.environ['DATABASE_URL'])
            DATABASES['default'] = {
                'NAME':     url.path[1:],
                'USER':     url.username,
                'PASSWORD': url.password,
                'HOST':     url.hostname,
                'PORT':     url.port,
            }
            if url.scheme == 'postgres':
                DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
            if url.scheme == 'mysql':
                DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
    except:
        print "Unexpected error:", sys.exc_info()


This is odd, not sure why this is like this since I'm seeing the DATABASES variable above. Let's check to see if the environment variables are there. (the output has been changed to protect the innocent, but you still get the picture). You can also use the command 'heroku config' if you just want to see your application configuration options.

.. code-block:: bash

    $ heroku run env
    Running env attached to terminal... up, run.6
    DATABASE_URL=postgres://blah:somethingelse@ec2-555-55-555-555.compute-1.amazonaws.com/morestuff
    PORT=37265
    HOME=/app
    PYTHONUNBUFFERED=true
    TERM=xterm
    COLUMNS=153

    PATH=bin:/usr/local/bin:/usr/bin:/bin
    PWD=/app
    SHARED_DATABASE_URL=postgres://blah:evenmorestuff@ec2-555-55-555-555.compute-1.amazonaws.com/morestuff
    LINES=32


This output looks good the DATABASE_URL env variable is there, so that is OK. Looking more closely at my settings.py file I didn't have a DATABASES variable because the last time I used this project, the other hosting provider didn't require that I have one. So I have added a blank DATABASES variable, and that seems to have fixed my issue. Heroku, should make the error message a little nicer, add more notes to their documentation, or even better make their code handle the case when there is no DATABASES variable in the settings file.  I have submitted a patch to fix this, so hopefully that will get rolled out in the near future. (https://github.com/heroku/heroku-buildpack-python/pull/8)


Now if we redeploy the app and look at the logs, they look much better.

.. code-block:: bash

    $ heroku logs
    2011-11-27T18:59:25+00:00 heroku[api]: Deploy 96be00f by kencochrane@
    2011-11-27T18:59:25+00:00 heroku[api]: Release v8 created by kencochrane@
    2011-11-27T18:59:25+00:00 heroku[web.1]: State changed from crashed to created
    2011-11-27T18:59:26+00:00 heroku[web.1]: State changed from created to starting
    2011-11-27T18:59:26+00:00 heroku[slugc]: Slug compilation finished
    2011-11-27T18:59:31+00:00 app[web.1]: 0 errors found
    2011-11-27T18:59:31+00:00 heroku[web.1]: State changed from starting to up

Running django management commands on Heroku
============================================

Running django management commands are easy you just need to run the following command and replace <command> with the management command you want to run. There are a few examples below.

.. code-block:: bash

    $ heroku run python kenblog/manage.py <command>

Running django shell on Heroku
------------------------------
If you need to use the interactive python shell with django, you still can, you just need to run the following command.

.. code-block:: bash

    $ heroku run python kenblog/manage.py shell


Syncing Django Database on Heroku
---------------------------------
Now that our application is starting like it should let's sync the db.

.. code-block:: bash

    $ heroku run python kenblog/manage.py syncdb

Running Django South Migrations on Heroku
-----------------------------------------

.. code-block:: bash

    $ heroku run python kenblog/manage.py migrate

Now lets look at our processes now

.. code-block:: bash

    $ heroku ps
    Process       State               Command
    ------------  ------------------  ------------------------------
    run.5         complete for 21m    cat kenblog/settings.py
    run.6         complete for 18m    env
    run.7         complete for 1m     python kenblog/manage.py syncdb
    run.8         complete for 1m     python kenblog/manage.py migrate
    web.1         up for 4m           python kenblog/manage.py runserver..

Things are looking better, we are up, and it also shows our old commands that we ran.

if you need to work with the processes you have the following options.

.. code-block:: bash

  ps:dynos [QTY]                 # scale to QTY web processes
  ps:restart [PROCESS]           # restart an app process
  ps:scale PROCESS1=AMOUNT1 ...  # scale processes by the given amount
  ps:stop PROCESS                # stop an app process
  ps:workers [QTY]               # scale to QTY background processes


Opening your django application in a web browser
================================================
If you run this command it will open a web browser and hopefully your site is running as it should

.. code-block:: bash

    $ heroku open


Running django and gunicorn on heroku
=====================================

By default heroku deploys with the built in django runserver, which isn't recommended for production. If you are playing around it is ok, but once you get past that, the first thing you should do is switch to something better like guincorn. Switching is quick and painless, and you will be glad that you did. 

1. Add gunicorn==0.13.4 to your requirements file.
2. create a new file called Procfile at the same level as your requirements.txt file with the following in it.

.. code-block:: bash

    web: python kenblog/manage.py run_gunicorn -b "0.0.0.0:$PORT" -w 3


Add gunicorn to the installed_apps in settings.py

then 

.. code-block:: bash

    $ git commit -am "use gunicorn"
    $ git push heroku master

Looking at your logs you will see it up and running

.. code-block:: bash

    $ heroku logs
    2011-11-27T21:06:24+00:00 heroku[slugc]: Slug compilation started
    2011-11-27T21:06:32+00:00 heroku[api]: Deploy 7b2eec1 by kencochrane@
    2011-11-27T21:06:32+00:00 heroku[api]: Release v8 created by kencochrane@
    2011-11-27T21:06:32+00:00 heroku[web.1]: State changed from created to starting
    2011-11-27T21:06:35+00:00 heroku[web.1]: Starting process with command `python kenblog/manage.py run_gunicorn -b "0.0.0.0:4075" -w 3`
    2011-11-27T21:06:36+00:00 app[web.1]: Validating models...
    2011-11-27T21:06:37+00:00 heroku[web.1]: State changed from starting to up


Running django/celery background tasks on Heroku
================================================
Heroku offers you two types of processes, a web process and a worker process. Web processes are used for serving web pages, etc. Worker processes are used for items that run in the background. The heroku tutorial goes over how to setup background task using celery and kombu (http://devcenter.heroku.com/articles/django) if you want more info I would check that out.


Serving Django Static media on Heroku
=====================================
I'm not sure how to serve up static media on heroku, to get my app working I just used the built in "django.views.static.serve" views for now, this isn't ideal and you would want a more permanent solution. A more long term solution would be to push all static media into Amazon s3 and then use Amazon cloudfront to serve everything.


Uploading files to Heroku with Django
=====================================
Heroku allows you to upload files to their app's "Emphemeral Filesystem": http://devcenter.heroku.com/articles/dyno-isolation#ephemeral_filesystem

    "Which the app can use as a temporary scratchpad, but no files it writes are visible to any other "Each dyno gets its own ephemeral filesystem, with a fresh copy of the most recently deployed code. During its lifetime the dyno can use the filesystem as a temporary scratchpad, but no files it writes are visible to any other dyno (including other dynos in the application) and any files written will be discarded the moment the dyno is stopped or restarted."

This means you can't use this space to store uploaded files, but it should allow you to upload it there for a minute, and then send it over to Amazon S3 for a more permant storage solution. You could use a tool like Django Queued storage for this: https://github.com/jezdez/django-queued-storage


Databases
=========

Heroku gives each app a 5MB shared postgresql database for FREE. If you pay $15/month you get upgraded to 20GB of space. They also offer dedicated database instances if you need that. See this page for more details. http://www.heroku.com/pricing#0-0

They also have a bunch of other addons (redis, mongodb, couchdb, amazon RDS) that you should be able to tie into, see the addons page for a complete list. http://addons.heroku.com/

Setting up Django Caching on Herku
==================================

To use memcache on Heroku, I went to the add-on page and installed the free memcache addon. Once I did this I can run the heroku config command to find out my config settings. I then use that information in my django settings file so that I can have access to caching in my app.

.. code-block:: bash

    $ heroku config
    ...
    MEMCACHE_PASSWORD    => xxxxxxxxxxxx
    MEMCACHE_SERVERS     => instance.hostname.net
    MEMCACHE_USERNAME    => xxxxxxxxxxxx
    ...

They also offer redis if you prefer that.

Sending Email from django on Heroku
===================================

If you need to send or receive email in your application there are a few email add-ons that you can use. Pick the one you want and then run the 'heroku config' command described above to get your settings, and update your django settings accordingly.


Application size
================
You application and all of it's dependencies can't be more then 100MB in size. 

Heroku Pricing
==============

Directly from this page: http://devcenter.heroku.com/articles/how-much-does-a-dyno-cost

Dynos cost $0.05 per hour, prorated to the second. For example, an app with four dynos is charged $0.20 per hour for each hour that the four dynos are running.

Pricing is based on calendar time. If you set your app to four dynos, you will be charged $0.20 per hour regardless of the traffic your site serves during that time.

Each application receives 750 free dyno hours per month. For example if you have 1 web dyno running for all of April, and a worker dyno running half the time you would have 330 dyno-hours billed that month or $16.50 (720 web dyno hours + 360 worker dyno hours - 750 free dyno hours).

See this page for more details: http://www.heroku.com/pricing#0-0

Conclusion
==========
I haven't really had much time to really play with Heroku, and stress test it at all, but I have to say it is pretty impressive to begin with. There are still some rough edges, but I'm sure they will have those smoothed out before they remove the beta tag. The thing that impresses me the most is all of the addons that you have access to out of the box. I'm not sure how many of these work with the new platform, or with django right now, but I'm sure it is only a matter of time before they are available.

I would highly recommend signing up and trying out their service, it is free so what do you have to lose?

Update
-------
2/16/2012: Full disclosure. On Feb 16th 2012, I accepted a job with dotCloud a competitor to Heroku. I plan on keeping this blog post up to date and impartial. If you think there are any errors, please let me know in the comments. 

