
:date: 2011-04-26 07:07:55
:tags: django,python,deployment,hosting,dotcloud,paas
:category: blog
:slug: deploying-my-django-application-to-dotcloud
:author: Ken Cochrane
:title: Deploying my Django application to dotCloud

.. warning::

    This post is out of date, please read the new updated one:

    `Deploying my Django application to dotCloud Part 2 <http://kencochrane.net/blog/2012/03/deploying-a-django-application-on-dotcloud/>`_



I have recently wrote about `ep.io <http://kencochrane.net/blog/2011/04/my-experiences-with-epio/>`_ and `gondor.io <http://kencochrane.net/blog/2011/04/my-day-gondorio/>`_, two new python/django hosting services that are currently in beta. Another new service that has just recently hit the scene and is causing a lot of waves is `DotCloud.com <http://dotcloud.com>`_. DotCloud is a little different for a number of reasons. Their service isn't targeting any one technology stack like ep.io and gondor.io with Python/Django/wsgi. 

DotCloud's goal is to provide a bunch of different independent services that you can use as building blocks to build your application. If you need a database, take your pick from one of the many they support. Need an application that uses Django or Rails on the front end, and Java in the backend, that is fine, you can do that too. They realize that most developers don't stick to one standard technology stack for all of their applications, so this allows you the flexibility to use the best tool for the job. It also gives you a nice playground to try out new services and see how they run without having to install, configure and maintain the service just for testing.

DotCloud was part of the Y Combinator summer class of 2010, and they just recently `raised $10 Million <http://techcrunch.com/2011/03/22/paas-dotcloud-raises-10m-from-jerry-yang-benchmark-and-others/>`_. With access to that much money, I'm guessing they will be hiring a bunch of people pretty quickly, and I'm sure we will be seeing their services expand as well. 

Like all new technologies, I want to play with them, and see if they live up to all of the hype. I was lucky enough to get a beta invite a few weeks ago, and I have been playing with it since. I decided that the best way to test it out would be to deploy my blog, and see how hard it would be. Here are the steps that I took to get my django based blog up and running on DotCloud. I ran into a few issues and I made sure that I put those in as well, so that if you get the same issue you can see how I solved it.


Documentation
=============


Before I get started with any new service the first thing I usually do is look at the documentation. DotCloud has a nice list of documents along with some tutorials on how to get started. These 3 documents were the ones that I used the most.


http://docs.dotcloud.com/tutorials/django/

http://docs.dotcloud.com/components/mysql/

http://docs.dotcloud.com/tutorials/firststeps/


First Steps:
============

Like all cool services these days, dotcloud uses a python based CLI, so before we can get started we need to install the dotcloud client and configure it so that we can start using it.

.. code-block:: bash
    
    # create my dotcloud virtual environment.
    $ mkvirtualenv dotcloud
    
    # install dotcloud client using pip
    $ pip install dotcloud
    
    # create our application namespace called kencochrane
    $ dotcloud create kencochrane
    
    #enter api key that we got from: http://www.dotcloud.com/account/settings when prompted
    #<key goes here>


Now that we have the client all setup, and an application namespace, now we can start building our service. I have forked my blog repository on bitbucket so that I could make dotcloud specific changes to it and not effect my original repo. 

.. code-block:: bash

    # go into projects directory
    cd ~/projects
    
    # forked kencochranenet to kencochranenet_dotcloud, now clone that. locally
    hg clone https://bitbucket.org/kencochrane/kencochranenet_dotcloud kencochrane_dotcloud
    
    # go into the new directory.
    cd kencochrane_dotcloud


Reading through the documentation tells me that I need to create a wsgi.py file and put in the root of my project. Using http://docs.dotcloud.com/tutorials/django/#djangowsgipy as a template, I created my wsgi.py file below. I had issues with the default template and I needed to add a directory to the sys.path so that wsgi could find my django apps correctly. Here is my finished file.

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

DotCloud requires that we put all of our static media in a directory called 'static' in the root of our project.  Because my static media is already found elsewhere, I need to create a directory called static and move all of my files into it. 

.. code-block:: bash

    # we need to create a static directory to serve static media from (/static) .
    mkdir -p static

If you use the django admin then you will need to create a postinstall script that will create a symlink under static for your django admin media files. Here is what mine looks like. If you use this as a template, don't forget to change the DJANGO_SETTINGS_MODULE variable to match your project.
    
.. code-block:: python
    
    #!/usr/bin/env python
    import os
    # To import anything under django.*, we must set this variable.
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
    # Import the admin module. The media directory is right under it!
    import django.contrib.admin
    # Retrieve the absolute path of the admin module.
    admindir = os.path.dirname(django.contrib.admin.__file__)
    # Add /media behind it.
    mediadir = os.path.join(admindir, 'media')
    # Compute the path of the symlink under the static directory.
    staticlink = os.path.join('static', 'admin_media')
    # If the link already exists, delete it.
    if os.path.islink(staticlink):
        os.unlink(staticlink)
    # Install the correct link. 
    
    os.symlink(mediadir, staticlink)
        
.. code-block:: bash

    # make the script executable.
    chmod +x postinstall


Because we changed our location of our static media, we need to remember to update our settings.py file with the new settings. Here are my changes.

.. code-block:: python

    # edit settings.py file to the following.
    ADMIN_MEDIA_PREFIX = '/static/admin_media/'
    
    # change MEDIA_URL
    MEDIA_URL = '/static/'


Deployment

Now that we have our application's project structure all setup and configured the way dotcloud wants it, we can start up some services and then deploy our app. If you want to find out what services they have available, you can run the following command.

.. code-block:: bash

    # find out which services that are available.
    dotcloud deploy -h

    You can chose among the following services:  
      java          host any Java servlet (also Clojure, Play!, and much more)
      mysql         the worlds most popular open source database             
      nodejs        run JavaScript processes (including web apps)             
      php           host any PHP web app: Drupal, WordPress...                
      php-worker    run background PHP processes                              
      postgresql    the worlds most advanced open source database            
      python        host any Python/WSGI web app: Django, Pylons, Web2py...   
      python-worker run background Python processes                           
      rabbitmq      AMQP message queue server                                 
      redis         advanced key-value store                                  
      ruby          host any Ruby/Rack web app: Rails, Sinatra...             
      ruby-worker   run background Ruby processes                             
      smtp          authenticated SMTP relay to send e-mails reliably         
      static        host static HTTP content    


We need a database for our blog, since it was originally setup to use mysql, lets use that one here. Start up a new mysql service called 'kencochrane.mysql'

.. code-block:: bash

    # start up the database service.
    $ dotcloud deploy -t mysql kencochrane.mysql
    Created "kencochrane.mysql".

Let's make sure that it was created, and find out some more about our new database instance.

.. code-block:: bash
    
    # get the information about our new service
    $ dotcloud info kencochrane.mysqlcluster: wolverine
    config:
        mysql_password: password_was_changed
    created_at: 1303671517.96066
    name: kencochrane.mysql
    namespace: kencochrane
    ports:
    -   name: ssh
        url: ssh://dotcloud@mysql.kencochrane.dotcloud.com:3912
    -   name: mysql
        url: mysql://root:password_was_changed@mysql.kencochrane.dotcloud.com:3913
    state: running
    type: mysql
    

As you can see from above, we have a mysql database, it is running, and it lets us know the ssh and mysql urls and ports, along with the root password. Lets create our database. To do that we will login to the server and run some sql commands. (the sensitive information has been changed)

.. code-block:: bash

    # connect to dotcloud mysql server instance
    $ dotcloud run kencochrane.mysql -- mysql -u root -p
    
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
    Shared connection to mysql.kencochrane.dotcloud.com closed.

Now that we have our database all setup, we need to change our settings file so that it has all of the new information. Here is what mine looks like.

.. code-block:: python

    # update your settings.py file.
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'blogdb',
            'USER': 'blog_username',
            'PASSWORD': 'strong_password',
            'HOST': 'mysql.kencochrane.dotcloud.com',
            'PORT': '3913',
        }
    }


Now we are ready to deploy our Django app, but before I go any further it is important to know the following. Dotcloud will pay attention to your .hgignore files. If you have a settings file in your .hgignore file so that it doesn't get saved in the repo, it will not push those changes up to the cloud. You will need to remove it from the .hgignore in order to get those files out there. It is also import to remember that only changes that are committed are pushed, so don't forget to commit your changes. If you wanted to be tricky you could use a post install script to pull down the file from a secure location and install it that way, if you want to make things super secure.

Now that we have that behind us, lets get going. First we need to create a new python service.

.. code-block:: bash

    # deploy a new python app called kencochrane.blog
    $ dotcloud deploy --type python kencochrane.blog

Service is now created so all we have to do is push our application to the new service.

.. code-block:: bash

    # push out your changes to the server
    $ dotcloud push kencochrane.blog .


Now your code is out in the cloud, you just need to sync your database and run the migrations to get your database all setup, and you should be good to go.

.. code-block:: bash

    # sync the database
    $ dotcloud run kencochrane.blog python current/mysite/manage.py syncdb
    
    # we use south so run migrate
    $ dotcloud run kencochrane.blog python current/mysite/manage.py migrate

now it works, just go to http://blog.kencochrane.dotcloud.com/ to see.

If you need to look at the logs to see how it is going you can do it two ways. The first way will tail your logs for you to your console.

.. code-block:: bash

    # look at logs of your service, it will tail them to your console. ctrl-c to stop.
    $ dotcloud logs kencochrane.blog
    
Or login via ssh and look at your logs.

.. code-block:: bash

    # Open up a shell
    $ dotcloud ssh kencochrane.blog


Here are the ones you most likely care about.

.. code-block:: bash

    # nginx access and error logs.
    /var/log/nginx/<app_name>.{access,error}.log
    
    # wsgi error logs
    /var/log/supervisor/uswgi.log


If you need to restart your service just issue this command.

.. code-block:: bash

    # restart the service
    dotcloud restart kencochrane.blog
    
DotCloud runs on Amazon's EC2 service, and last week while I was doing my testing, I was getting a bunch of errors, I wasn't sure if the errors were because this is a beta service, and they are still bugs in it, or if it was related to the amazon issues. Either way, I listed those errors below incase anyone else gets them. If I got the error I would just run the command again until it worked, sometimes it took 3 times before everything worked fine.

.. code-block:: bash

    # attempt 1
    $ dotcloud push kencochrane.blog .DotCloud service unavailable ("No JSON object could be decoded").
    Please try again later. If the problem persists, send an email to support@dotcloud.com.
    
    # attempt 2
    $ dotcloud push kencochrane.blog .
    # upload . ssh://dotcloud@uploader.dotcloud.com:1060/kencochrane.blog
    # hg
    remote: Warning: Permanently added '[uploader.dotcloud.com]:1060,[174.129.15.77]:1060' (RSA) to the list of known hosts.
    pushing to ssh://dotcloud@uploader.dotcloud.com:1060/kencochrane.blog
    searching for changes
    remote: adding changesets
    remote: adding manifests
    remote: adding file changes
    remote: added 1 changesets with 3 changes to 3 files
    Scheduling build
    Fetching logs...
    Build started...
    mkdir: cannot create directory `126:afdea9036e83': File exists
    Failed to fetch tarball (<type 'exceptions.ValueError'>: Failed to extract the tarball, abort.)
    Build finished.
    Shared connection to blog.kencochrane.dotcloud.com closed.

    # 3rd time is a charm, it finally works.
    $ dotcloud push kencochrane.blog .# upload . ssh://dotcloud@uploader.dotcloud.com:1060/kencochrane.blog
    # hg
    remote: Warning: Permanently added '[uploader.dotcloud.com]:1060,[174.129.15.77]:1060' (RSA) to the list of known hosts.
    pushing to ssh://dotcloud@uploader.dotcloud.com:1060/kencochrane.blog
    searching for changes
    no changes found
    Scheduling build
    Fetching logs...
    Build started...
    .
    . all of the files (trimmed for space)
    .
    Fetched code revision 126:afdea9036e83
    .
    . all the requirments (trimmed for space)
    .
    Cleaning up...
    Reloading nginx configuration: nginx.
    uwsgi: stopped
    uwsgi: started
    Build finished.

    Shared connection to blog.kencochrane.dotcloud.com closed.


Conclusion:
===========

Setting up my blog on DotCloud was fairly straightforward, the documentation helped guide me along the way. I did run into a few road blocks that stopped me in my tracks for a little while, but after some digging I was able to get past those issues. Hopefully this post will help you overcome the same issues I had, and make your deployment a little more smooth.

The service is very flexible, which is going to be good for most developers, but with the added flexibility they added some complexity that doesn't exist on the other services. For example ep.io and gondor.io handle all database and user creation for you, so you don't need to know what commands to run to create the database and the user, and they also automatically add the database connection strings to your settings file. I for one don't mind the extra complexity considering I'm going to get the ability to have direct access to my database so that I can do what I want. Others, might not want to worry about that. If you are building an application for a client that isn't very tech savy, the more things that are automated the better.


DotCloud is still in beta, and if you take a look at their `roadmap <http://docs.dotcloud.com/components/roadmap/>`_, they have very ambitious goals. I for one can't wait to see how they progress. I have only gone into a few of the many things that dotcloud has to offer, I recommend that you try it out for yourself and leave me a comment letting me know how you liked it.


Next time:
==========

I have been lucky enough to get a sneak peak at http://apphosted.com a python/django hosting service similar to gondor.io and ep.io. I'm currently playing with the service now, once I'm finished I'll post my findings.


Update:
-------
Read how this service stacks up against other services like it in my `Django hosting roundup <http://kencochrane.net/blog/2011/06/django-hosting-roundup-who-wins/>`_

2/16/2012: Full disclosure. On Feb 16th 2012, I `accepted a job with dotCloud <http://kencochrane.net/blog/2012/03/im-now-working-for-dotcloud/>`_. I plan on keeping this blog post up to date and impartial. If you think there are any errors, please let me know in the comments. 


.. warning::

    This post is out of date, please read the new updated one:

    `Deploying my Django application to dotCloud Part 2 <http://kencochrane.net/blog/2012/03/deploying-a-django-application-on-dotcloud/>`_

