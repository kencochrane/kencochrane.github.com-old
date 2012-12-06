
:date: 2012-03-23 14:58:01
:tags: dotcloud,django,paas,python,hosting,deployment
:category: blog
:slug: deploying-a-django-application-on-dotcloud
:author: Ken Cochrane
:title: Deploying my Django application to dotCloud: Part 2


As I mentioned in a `recent blog post <http://kencochrane.net/blog/2012/03/im-now-working-for-dotcloud/>`_, in the 11 months since I wrote my `first post on dotCloud <http://kencochrane.net/blog/2011/04/deploying-my-django-application-to-dotcloud/>`_, I now work there. Besides me working there, there has been a lot of other changes at `dotCloud <http://www.dotcloud.com>`_, and I wanted to take the time to update my original post so that it was up to date and had all the recent information. I'm going to completely rewrite the old blog post here, with updated information, and leave the old one around for posterity.

dotCloud's goal is to provide a bunch of different independent services that you can use as building blocks to build your application. If you need a database, take your pick from one of the many they support. Need an application that uses Django or Rails on the front end, and Java in the backend, that is fine, you can do that too. They realize that most developers don't stick to one standard technology stack for all of their applications, so this allows you the flexibility to use the best tool for the job. It also gives you a nice playground to try out new services and see how they run without having to install, configure and maintain the service just for testing.

I'm going to go over the steps that it took to install my blog onto dotCloud, and hopefully answer some common questions along the way.


Documentation
=============

Before I get started with any new service the first thing I usually do is look at the documentation. DotCloud has a nice list of documents along with some tutorials on how to get started. These 4 documents were the ones that I used the most.

http://docs.dotcloud.com/firststeps/platform-overview/

http://docs.dotcloud.com/tutorials/python/django/

http://docs.dotcloud.com/services/mysql/

http://docs.dotcloud.com/services/mysql-masterslave/


First Steps:
============

Like all cool services these days, dotCloud uses a python based CLI, so before we can get started we need to install the dotCloud client and configure it so that we can start using it.

.. code-block:: bash
    
    # create my dotcloud virtual environment.
    $ mkvirtualenv dotcloud
    
    # install dotcloud client using pip
    $ pip install dotcloud
    
    # create our application called blog
    $ dotcloud create blog
    
    #enter api key that we got from: http://www.dotcloud.com/account/settings when prompted
    #<key goes here>
    
    # if you were not prompted to enter your key you can run this command, and it will let you enter your API key again.
    $ dotcloud register


Now that we have the client all setup, and an application created, now we can start building our service. I have forked my blog repository on github so that I could make dotCloud specific changes to it and not effect my original repo. 

.. code-block:: bash

    # go into projects directory
    cd ~/projects
    
    # forked kencochranenet to kencochranenet_dotcloud, now clone that. locally
    git clone git://github.com/kencochrane/kencochranenet_dotcloud.git kencochranenet_dotcloud
    
    # go into the new directory.
    cd kencochrane_dotcloud


Reading through the documentation tells me that I need to create a wsgi.py file and put in the root of my project. Using http://docs.dotcloud.com/tutorials/python/django/#wsgi-py as a template, I created my wsgi.py file below. I had issues with the default template and I needed to add a directory to the sys.path so that wsgi could find my django apps correctly. Here is my finished file.

.. code-block:: python

    import os
    import sys
    
    # Ken added this, only thing that is different from the example template (not counting settings file name)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'mysite')))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
    
    import django.core.handlers.wsgi
    djangoapplication = django.core.handlers.wsgi.WSGIHandler()
    def application(environ, start_response):
        if 'SCRIPT_NAME' in environ:
            del environ['SCRIPT_NAME']
        return djangoapplication(environ, start_response)
    

DotCloud uses `PIP requirements files <http://www.pip-installer.org/en/latest/#requirements-files>`_ to manage your project dependencies. We already have our pip requirements file where it needs to be and named correctly so we don't need to do anything, but if we didn't have one, we would need to create one and put it in the root, and call it requirements.txt

Services
--------
When we add a service to our deployment stack, dotCloud gives us the appropriate connection information in a file called '/home/dotcloud/environment.json' that is available to us on our deployment container. This allows us to not have to hard code username/password and server urls in our settings.py file, and it also makes it a little more secure for us since we don't have to have that info in our source repository. 

This is how we use it. At the top of your settings.py file you will need to add the following. snippet.

.. code-block:: python

    import json
    with open('/home/dotcloud/environment.json') as f:
      env = json.load(f)


Once we have that added to the settings.py file, we now have a variable env that has all of the env settings we need. 

You could go a little further add some custom code to check if the environment.json file exists, and if it does, you know you are in production, so use that setup, or if not, then you must be in local mode, so use your local settings. If you want to get really cool, you can have your own json file that has a similar setup for local development, and if it doesn't find the dotcloud one, it could look for your own, and load your settings from that. This will allow you to use the same settings file for both production and dev, with only a little bit of code at the top to load the correct env file.

Database
--------
Most applications need a database, and this blog is no different. This is how we setup our database to work with our blog on dotcloud. We are going to be using mysql for our database. With Django you need to set your database settings in your settings.py. This is how we setup a mysql database connection inside of our settings.py. Notice that the name of the database doesn't come from the env, you pick that yourself. 

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'blogdb',
            'USER': env['DOTCLOUD_DB_MYSQL_LOGIN'],
            'PASSWORD': env['DOTCLOUD_DB_MYSQL_PASSWORD'],
            'HOST': env['DOTCLOUD_DB_MYSQL_HOST'],
            'PORT': int(env['DOTCLOUD_DB_MYSQL_PORT']),
        }
    }


Create the Database
-------------------
dotCloud gives you your own dedicated database, with full root access. With great power comes great responsibilities. One of those responsibilities is that you need to create your own database schemas, and users yourself. Which means you normally need to do something like this.

.. code-block:: bash

    # connect to dotcloud mysql server instance
    $ dotcloud run blog.db -- mysql -u root -p
    
    # mysql -u root -p
    Enter password:
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 34
    Server version: 5.1.41-3ubuntu12.10 (Ubuntu)

    # create the user and database and give user permissions to database.
    
    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
    
    mysql> create database blogdb;
    Query OK, 1 row affected (0.00 sec)
    
    mysql> create user 'blog_username' identified by 'strong_password';
    Query OK, 0 rows affected (0.05 sec)
    
    mysql> grant all on blogdb.* to 'blog_user'@'%';
    Query OK, 0 rows affected (0.04 sec)
    
    mysql> flush privileges;
    Query OK, 0 rows affected (0.00 sec)
    
    mysql> exit;Bye
    Shared connection to database closed.

Does that look familiar? I have it here in case you want to do it the long way.

To make things easier, we are going to create a small python script that will check to see if we have our database created, and if not, it will create it for us. This will make it so that we don't have to login into our database and do it by hand before we deploy. The file is called createdb.py and this is what it looks like. This script is for mysql. If you want a postgreSQL database, you can use this as a template and change it so that it will work with postgreSQL.

.. code-block:: python

    import MySQLdb
    import os
    from wsgi import *
 
    def create_dbs(names):
        print("create_dbs: let's go.")
        django_settings = __import__(os.environ['DJANGO_SETTINGS_MODULE'], fromlist='DATABASES')
        print("create_dbs: got settings.")
        databases = django_settings.DATABASES
        for name, db in databases.iteritems():
            if name in names and db['ENGINE'].endswith('mysql'):
                host = db['HOST']
                user = db['USER']
                password = db['PASSWORD']
                port = db['PORT']
                db_name = db['NAME']
                print 'creating database %s on %s' % (db_name, host)
                db = MySQLdb.connect(user=user,
                                    passwd=password,
                                    host=host,
                                    port=port)
                cur = db.cursor()
                print("Check if database is already there.")
                cur.execute("""SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA 
                             WHERE SCHEMA_NAME = %s""", (db_name,))
                results = cur.fetchone()
                if not results:
                    print("Database %s doesn't exist, lets create it." % db_name)
                    sql = """CREATE DATABASE IF NOT EXISTS %s """ % (db_name,)
                    print("> %s" % sql)
                    cur.execute(sql)
                    print(".....")
                else:
                    print("database already exists, moving on to next step.")


    if __name__ == '__main__':
        import sys
        print("create_dbs start")
        create_dbs(sys.argv[1:])
        print("create_dbs all done")


Adding a cache
--------------

Since most of the blog content doesn't change much, it is a great candidate for caching. So we are going to take advantage of Django's built in caching abilities and add some caching to our blog. Normally I use `memcached <http://memcached.org>`_ for my caching, but dotCloud's memcached support is limited right now. The reason why it is limited is because memcached doesn't have any built in authentication mechanism, and in order to make sure it is secure, you need to run a special version of memcached that supports `SASL <http://code.google.com/p/memcached/wiki/SASLAuthProtocol>`_, and most of the memcached clients don't support this. So instead of deploying an insecure service, they decided to not support it fully. There are ways to use it, but it involves all kind of complicated firewall rules and running something like stunnel. So it is possible, but it isn't very clean. 

Instead they recommend that you use `redis <http://redis.io>`_ instead, redis has the same caching abilities that memcached has, plus a lot more, including authentication. So we are going to use redis for our cache. In order to use redis, we will need to add the redis library because redis caching support isn't built into Django. In your requirements.txt file you will need to add ``django-redis==1.4.5`` so that the libraries will be available for Django to use.

Once you have the library installed, you will need to add these settings to your settings.py file so that django knows which redis server and password to use.

.. code-block:: python

    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.cache.RedisCache',
            'LOCATION': env['DOTCLOUD_CACHE_REDIS_HOST']+':'+env['DOTCLOUD_CACHE_REDIS_PORT'],
            'OPTIONS': {
                'DB': 1,
                'PASSWORD': env['DOTCLOUD_CACHE_REDIS_PASSWORD'],
                'PARSER_CLASS': 'redis.connection.HiredisParser'
            },
        },
    }

    # we also are going to use redis for our session cache as well.
    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'


For more information about using redis as your cache for Django, check out these links.

- https://github.com/niwibe/django-redis

- http://pypi.python.org/pypi/django-redis/1.4.5

- https://docs.djangoproject.com/en/1.3/topics/cache/

- http://answers.dotcloud.com/question/213/redis-cache-settings-for-django

Django Admin
------------
We also need an easy way to create our django admin account for us. In order to do that I have this mkadmin.py script. This will default the password to 'P@s$w0rd1', once you have your code installed, you will need to login to the admin account and change your password to something more secure.

.. code-block:: python

    #!/usr/bin/env python
    from wsgi import *
    from django.contrib.auth.models import User
    u, created = User.objects.get_or_create(username='admin')
    if created:
        u.set_password('P@s$w0rd1')
        u.is_superuser = True
        u.is_staff = True
        u.save()


Media
-----
We need to put our static and media files in the following locations: ``static=/home/dotcloud/data/static/`` and ``media=/home/dotcloud/data/media/``. Because of this we need to make sure we change our settings.py file, and setup an nginx.conf file to map to the correct locations. Here are the settings.py file changes.

.. code-block:: python

    # media settings
    MEDIA_ROOT = '/home/dotcloud/data/media/'
    MEDIA_URL = '/media/'

    # static settings
    STATIC_ROOT = '/home/dotcloud/data/static/'
    STATIC_URL = '/static/'

    # admin prefix
    ADMIN_MEDIA_PREFIX = '/static/admin/'

Here is the nginx.conf

.. code-block:: nginx

    location /media/ { root /home/dotcloud/data ; }
    location /static/ { root /home/dotcloud/data ; }

Post Install
------------
We are going to create a `postinstall <http://docs.dotcloud.com/guides/postinstall/>`_ script to handle all of the tasks we need to do after we install our code on the server. This is what will call our createdb.py, and mkadmin.py files from above, as well as syncing our database, running migrations and running collectstatic to move all static files into the right locations.
    
.. code-block:: bash
    
    #!/bin/sh
    python createdb.py default
    python mysite/manage.py syncdb --noinput
    python mysite/manage.py migrate
    python mkadmin.py
    mkdir -p /home/dotcloud/data/media /home/dotcloud/data/static
    python mysite/manage.py collectstatic --noinput


Don't forget to make sure your postinstall, createdb.py and mkadmin.py scripts are executable.

.. code-block:: bash

    # make the script executable.
    $ chmod +x postinstall createdb.py mkadmin.py



dotcloud.yml
------------
Now that we have our application's project structure all setup and configured the way dotCloud wants it, we can configure our deployment stack. This is done with a file called dotcloud.yml. For more information about the dotcloud.yml file check out this link: http://docs.dotcloud.com/guides/build-file/

.. code-block:: yaml

    www:
      type: python
    db:
      type: mysql
    cache:
      type: redis

This is telling us that we want 3 services, a python www service, a mysql db service, and a redis cache service. This is a very basic setup, and you can get a lot more complicated depending on what you want to achieve. Notice that this isn't setup for high availability because none of the instances are scaled. See the section about scaling below for more information. If you are running in a production app on dotCloud it is recommended that you scale all of your services so that they can withstand EC2 server crashes, and other unforeseen issues. 


Deployment
----------
Now we are ready to deploy our Django app, but before I go any further it is important to know the following. Dotcloud will pay attention to your .gitignore files. If you have a settings file in your .gitignore file so that it doesn't get saved in the repo, it will not push those changes up to the cloud. You will need to remove it from the .gitignore in order to get those files out there. It is also import to remember that only changes that are committed are pushed, so don't forget to commit your changes. If you wanted to be tricky you could use a post install script to pull down the file from a secure location and install it that way, if you want to make things super secure.

Everything is all setup, so all we have to do is push our application to dotCloud.

.. code-block:: bash

    # push out your changes to the server
    $ dotcloud push blog .


Service info
------------
Once you push your code to dotCloud you can see what it looks like by running the info command. 

.. code-block:: bash

    # get the information about our new services
    $ dotcloud info blog
    cache:
        config:
            redis_password: <password>
            redis_replication: true
        instances: 1
        type: redis
    db:
        config:
            mysql_masterslave: true
            mysql_password: <password>
        instances: 1
        type: mysql
    www:
        config:
            static: static
            uwsgi_processes: 4
        instances: 1
        type: python
        url: <url was here>


Scaling
-------
Scaling is the ability to grow your application so that it can handle more traffic, or possible failures that might occur. With a normal non PaaS setup, scaling an application can be quite painful and time consuming, but with a PaaS it can be as easy as running a few commands. There are three types of scaling, Vertical, Horizontal, High Availability. 

Vertical scaling, means growing the service you have now so that it can get bigger. This is popular with databases, the bigger a database gets the more space and memory it needs. 

Horizontal scaling means creating more then one instance of a service so it spread the work between the different services, giving you greater capacity.

High Availability means that you have more then one service running at a time, so that if one of the services has an issue, the other one will pick up the slack. This will help avoid downtime, when failures occur (EC2 instance crashes). Ideally when running in production, all of your services should be scaled for High Availability.

There are two kinds of services, stateful, and stateless. Stateful services are services that holds persistent data. Examples of stateful services are mysql, redis, postgresql, solr, MongoDB and RabbitMQ.

Horizontally High availability scaling a stateful service on dotCloud means creating a master/slave setup, which can switch the slave with the master automatically if the master has any issues. dotCloud supports HA scaling on MySQL, redis, and MongoDB.

Stateful services scale like this

  - mysql : 2 (master/slave)
  - redis : 2 (master/slave)
  - mongodb : 3 or 5 (using replica sets)

Scaling a stateless and one of the supported stateful services is the same. You would just run the scale command line command.

.. code-block:: bash

    $ dotcloud scale app db=2

For stateless applications, you are limited to a set number of scaling units, unless you are on the enterprise plan. If you need to have an application with lots of scale units, you should contact dotCloud, and let them know what you are planning to do, and they will advise you on how best to accomplish your goals.

Link: http://docs.dotcloud.com/guides/scaling/


Database Backups
----------------
Just because you are hosting your application on dotCloud doesn't mean you shouldn't backup your data. The most important data to backup is your database. Luckily dotCloud makes it easy to back up your database. There is a very helpful guide on how to setup your database backups here: http://docs.dotcloud.com/guides/backups/

Email
-----
If you need to send or receive email from your application, you can do that to. Because dotCloud runs on EC2, and EC2 is a popular place where SPAMMERS send SPAM from, it is best to use a 3rd party email provider to send your emails for you. Popular ones are `MailGun <http://mailgun.net/>`_, `SendGrid <http://sendgrid.com/>`_, `CritSend <http://www.critsend.com/>`_, and `Amazon SES <http://aws.amazon.com/ses/>`_. 

You can set this up a couple of different ways. The first way is the easiest way possible, it allows you to configure the SMTP settings for each service. You would do it like this (see below). You can manually set the smtp settings for that service, and when your application needs to send an email it will use those settings. This is the most simple setup, but there are downsides to this approach. You would need to set this for each service, if you have more then one that will be duplicated everywhere. Also if you want to change your settings, you will need to destroy your service and recreate it, since those configs can only be set once when the service is created.

.. code-block:: yaml

    www:
      type: python
      config:
        smtp_server: smtp.mailgun.org
        smtp_port: 25
        smtp_username: postmaster@company.com
        smtp_password: YourMailGunPassword


A better approach would be to use dotCloud's SMTP service. The SMTP service is built to receive emails from your services and forward them to the appropriate location. It is best to use a 3rd party email provider, but you can also use the typical poor mans solution, where you use gmail to send your emails. Be careful when using gmail, because you aren't aloud to send a lot of emails via gmail, once you hit your daily limit you will be blocked, so this is fine for a few emails a day, don't trust it for everyday stuff. Also, the emails will always be coming from your gmail address, fine for system emails, but not if you are trying to run a legit business.


Here is an example using mailgun.

.. code-block:: yaml

    mailer:
      type: smtp
      config:
        smtp_relay_server: smtp.mailgun.org
        smtp_relay_port: 587
        smtp_relay_username: postmaster@yourmailgundomain.com
        smtp_relay_password: YourMailgunPassword
    
Here is an example using gmail.

.. code-block:: yaml

    mailer:
      type: smtp
      config:
        smtp_relay_server: smtp.gmail.com
        smtp_relay_port: 587
        smtp_relay_username: your_gmail_username@gmail.com
        smtp_relay_password: Your_Gmail_Password


Once you have these all setup, they will be available in your environment.json file.


If you want to receive email, it is best to use a service like `MailGun <http://mailgun.net/>`_ . 

Links:

- http://docs.dotcloud.com/guides/emails/
- http://docs.dotcloud.com/services/smtp/


Cron jobs
---------
If your app needs to run cron jobs, follow the steps in this guide: http://docs.dotcloud.com/guides/periodic-tasks/

Celery
------
This blog doesn't really have a need for celery, but dotCloud does support it. For more information follow this link: http://docs.dotcloud.com/tutorials/python/django-celery/

S3FS
----
If you store data on s3 you can mount your s3 bucket so that you can have access to s3 from your application, just like it was a local directory on your container. This is helpful for storing files that are uploaded by your visitors, or to share files between different web processes. Follow these instructions to set it up: http://docs.dotcloud.com/guides/s3fs/

Logs
----
If you need to look at the logs to see how it is going you can do it two ways. The first way will tail your logs for you to your console.

.. code-block:: bash

    # look at logs of your service, it will tail them to your console. ctrl-c to stop.
    $ dotcloud logs blog.www
    
Or login via ssh and look at your logs.

.. code-block:: bash

    # Open up a shell
    $ dotcloud ssh blog.www


Here are the ones you most likely care about.

.. code-block:: bash

    # nginx access and error logs.
    /var/log/nginx/<app_name>.{access,error}.log
    
    # wsgi error logs
    /var/log/supervisor/uswgi.log


Restart Service
---------------
If you need to restart your service just issue this command.

.. code-block:: bash

    # restart the service
    dotcloud restart blog.www
    

Links
-----
- Read how this service stacks up against other services like it in my `Django hosting roundup <http://kencochrane.net/blog/2011/06/django-hosting-roundup-who-wins/>`_
- http://www.dotCloud.com

