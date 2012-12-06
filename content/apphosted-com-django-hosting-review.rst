
:date: 2011-05-18 12:17:48
:tags: django,hosting,apphosted,python,deployment,paas
:category: blog
:slug: apphosted-com-django-hosting-review
:author: Ken Cochrane
:title: AppHosted.com Django Hosting Service Review


This post is the fourth in my series about the new Django hosting services that just recently hit the market. Previously I have reviewed `ep.io <http://kencochrane.net/blog/2011/04/my-experiences-with-epio/>`_ , `gondor.io <http://kencochrane.net/blog/2011/04/my-day-gondorio/>`_ , and `dotCloud.com <http://kencochrane.net/blog/2011/04/deploying-my-django-application-to-dotcloud/>`_ .This post reviews `AppHosted.com <http://AppHosted.com>`_ , another similar service that is currently in beta. I was lucky enough to get a sneak peak of this service before it was released to the general public, and here are my notes and impressions for the short time I had to play with the new service.

Overview
========

`AppHosted.com <http://AppHosted.com>`_ uses a similar concept as the other django hosting services, they provide you with a command line client called metro that you use to interact with the service. Like the other command line clients, it is pretty much just a nice wrapper around their API, so anything you can do with the metro client you can do with their API. The client is used to configure your service and push your files up into their servers. Once the application is created and your code has been uploaded to their server, you can use their web based control panel to configure or manage your application.

So that we can compare apples to apples I will go through the process of installing my blog onto the service so that we can see how it works with apphosted compared to the other services. It will also hopefully provide a very simple how to guide on how to install your application onto AppHosted.com.

First Steps
===========

Like all new projects the first thing that I like to do is create a new project directory and a new virtual environment for the project.

.. code-block:: bash

    # move into my projects directory
    $ cd ~projects/

    # make my virtual environment apphosted
    $ mkvirtualenv apphosted
    
    # clone my blog
    $ hg clone https://bitbucket.org/kencochrane/kencochranenet kencochrane_apphosted
    
    # move into the new project directory 
    $ cd kencochrane_apphosted


Now that I have a local working copy of my blog code and a new virtual environment I'm ready to go.


Command Line Interface
======================

AppHosted has a command line client called Metro, it uses this client to configure and upload your application onto the apphosted servers. Metro only has three dependencies: httplib2, paramiko, and pycrypto, if you don't have them installed pip should handle that for you.

.. code-block:: bash

    # install the metro client
    $ pip install metroclient
    
    Downloading/unpacking metroclient
    Running setup.py egg_info for package metroclient
    Requirement already satisfied (use --upgrade to upgrade): httplib2 in /Users/ken/.virtualenvs/apphosted/lib/python2.6/site-packages (from metroclient)
    Requirement already satisfied (use --upgrade to upgrade): paramiko in /Library/Python/2.6/site-packages (from metroclient)
    Requirement already satisfied (use --upgrade to upgrade): pycrypto>=1.9 in /Library/Python/2.6/site-packages (from paramiko->metroclient)
    Installing collected packages: metroclient
    Running setup.py install for metroclient
    changing mode of build/scripts-2.6/metro from 644 to 755
    changing mode of /Users/ken/.virtualenvs/apphosted/bin/metro to 755
    Successfully installed metroclient


Initial Data & Django admin user
================================

At the moment Apphosted.com doesn't provide an easy way to create a django admin user, in order to create this user in your appHosted.com database you need to create it on a local database and then export that data into a fixture called initial_data.json. 

.. code-block:: bash

    # locally I run this command to dump the data, so that I can load on app hosted.
    $ python manage.py dumpdata > initial_data.json

There is another way to create the django admin user, which I'll describe a little later. This would also be the same way that you would import any application data that you need in order for your application to run correctly. 

Metro Client
============

One of the goals for appHosted.com was that they didn't want to require that you make lots of changes to your project directory structure  in order to use their service. In order to do this they need to do a lot more work to figure out what it is you want to do, and if they can't figure it out, they will ask you some questions. 

Now that we have our project directory and our initial_data.json file all ready, lets go ahead and deploy the application. Activate the virtual environment and go into your project directory. Kick off the metro client and answer the questions that pop up.

.. code-block:: bash

    # run the metro client.
    $ metro
    
    Metro Application Manager 1.21
    Copyright (c) Lumentica,  http://www.lumentica.com
    
    Application directory (i.e. path to project): ./
    Application name: kencochraneblog
    Application version: 0.1
    Application description: Ken's AppHosted Blog
    Application modules (extra; comma-separated): South==0.7.3, django-activitysync==0.2.2, django-debug-toolbar==0.8.4, django-disqus==0.3.4, django-memcache-status==1.0.1, django-tagging==0.3.1, django-xmlrpc==0.1.2, feedparser==4.1, httplib2==0.6.0, oauth2==1.2.0, python-memcached==1.47, python-twitter==0.8.1, simplejson==2.1.2, wsgiref==0.1.2, yolk==0.4.1, docutils==0.6, Pygments==1.3.1
    WSGI module (optional):
    Paste config (optional):
    Fixtures (optional; comma-separated):
    Sync database and load fixtures? (y/n): y
    Use SSL? (y/n): n
    Force SSL: (y/n): n
    Build complete.
    Upload to AppHosted? (y/n): y
    AppHosted Username: kencochrane
    AppHosted Password:
    Deploying...
    :: Configuring application environment...
    :: Configuring application permissions...
    :: Configuring application server...
    :: Application deployed to server successfully...
    :: Application deployment complete...



What did this do for us? It takes our application, and uploads it to their server, and then it installs all of our dependencies that we listed above. Then it configures it according to our answers, and tries to start it up, if we told it to, it will sync our database and load our fixtures. It also takes all of this information and stores it in a file called metro.config, so that we don't need to type that in every time if nothing has changed.

You might have noticed that I needed to manually enter in all of my dependencies when prompted, when I asked about this, I was told that if I didn't enter all of the dependencies it would scan the project for a pip style requirements.txt file, and use that to load all of your dependencies. I haven't had a chance to test that out yet, since I already entered my requirements by hand, and once you do it, you don't need to do it again.

My blog uses south for migration management, and at the time of this writing there is a bug, and it isn't correctly kicking off the migrate command during the database sync process. They are aware of the issue and they are working on a fix, but there is a work around in the meantime. I'll describe the work around shortly.

Once your application is deployed it will almost immediately be available at http://<your-app-name>.apphosted.com.

Log Files
=========

In order to view the log files, you need to log into the web control panel and from there you can download the logs that you are interested in. At the moment they only support downloading the log files, which is a little inconvenient, it would be nice to have the ability to tail the logs, or see the last 50 or 100 lines in the control panel. I asked about this, and they agreed and said it is on their list of things to work on.

Shell Access
============

Metro gives you the ability to shell into your application directory, so that you can kick off django management commands, and other cool things. One important thing to note is that when you login to the shell, it is a jailed shell, and you only have access to your own project, and with limited command access. This is done for security reasons. It is nice to know that your application runs in it's own jailed area, and no one else's applications can access your information.

Setting up the shell access requires a few steps. Follow these directions to get the full details: http://docs.apphosted.com/apphosted/apphosted_shell.html , but basically it requires the following.

1. create a ssh key if you don't already have one.
2. Login to the web console and add your public key.
3. In the web console browse over to your application Settings->Tools page and click on the “Update Public Keys” button. (Don't forget about this step, or you won't be able to login.
4. Use the metro client to open the shell. 

*Note*: It would be real cool if we didn't have to do step 3, why can't it automatically update the public keys for all apps? I'm guessing it is a security reason. The first time, I didn't hit the update public keys button and I couldn't figure out why it wasn't working, and luckily one quick email to the support line, and they let me know what I did wrong, and I was up and running in no time.

This is how you can kick off the shell, there are a bunch of command line args that you can pass as well, just do metro --help and it will show them all to you. 

.. code-block:: bash

    $ metro -s

*Note*: There is currently a bug that is preventing me from logging into the shell from my MacBook Pro OS X 10.6.7 using Python 2.6.1 . When I do it gives me this error. I have informed appHosted, and they said it looks like an issue with paramiko and python 2.6.1 on the Mac, not sure if it affects other python versions on other operating systems. They are working on the issue.

.. code-block:: bash

    $ metro -s
    Metro Application Manager 1.21
    Copyright (c) Lumentica,  http://www.lumentica.com
    
    Application name: kencochraneblog
    AppHosted Username: kencochrane
    AppHosted Password:
    Traceback (most recent call last):
    File "/Users/ken/.virtualenvs/apphosted/bin/metro", line 75, in run_shell
    ssh.connect(host, username=app_name, port=port)
    File "/Library/Python/2.6/site-packages/paramiko/client.py", line 278, in connect
    for (family, socktype, proto, canonname, sockaddr) in socket.getaddrinfo(hostname, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
    gaierror: [Errno 8] nodename nor servname provided, or not known
    Error: [Errno 8] nodename nor servname provided, or not known


Work Arounds
============

Now that you know how to shell into your application, you can also kick off django management commands. I mentioned earlier that there was another way to create the django admin user, well here is how you do it. Login to the metro shell and then kick off the createsuperuser django management command. Logging into the shell and finding things isn't easy do to the added security so to save you some trouble this is what I did. Python isn't in your path so you need to put the fully qualified path to the virtual env's python. Not sure if the jailed shell allows you to edit your .profile if so, it might be nice to configure this so that you don't always have to do the full path.

.. code-block:: bash

    # Create superuser (django admin)
    $ /ve/kencochraneblog/bin/python /app/kencochraneblog/mysite/manage.py createsuperuser
    
    # kicking off south migrations by hand.
    $ /ve/kencochraneblog/bin/python /app/kencochraneblog/mysite/manage.py migrate
    
My application's name is kencochraneblog, so make sure you replace my application name with yours, it should be something like this. replace app_name,django_project_dir and command with your variables.

.. code-block:: bash

    $ /ve/<app_name>/bin/python /app/<app_name>/<django_project_dir>/manage.py <command>
    

Background Tasks
================

AppHosted also supports background tasks via celery, they don't have the documentation created yet, but it should be available soon. They are also planning on supporting a cron like service, not sure if it will be cron, or something similar, but it should do, what you need it to do.

API
===

AppHosted provides a pretty nice API that allows you to do anything that the metro client does. This will allow you to write your own automation and management scripts to interact with your application. If you practice continuous deployment, it will allow you to automatically deploy the latest version of code on a post commit hook, if all of your tests pass.

Services
========

Right now they only support memcache for caching, and PostgreSQL for databases, but they plan on adding more services as they move forward.

Conclusion
==========

I have been playing with AppHosted for a few weeks now, and I'm pretty happy with what they have so far. They still have a few issues to work out and they are still a work in progress, but I have been seeing improvements all of the time, so it will only be a matter of time before they are ready for the general public. Every time I came across an issue, they were quick to reply to my emails and solve my issues, or tell me where I was going wrong.  If you have any more questions I recommend checking out their documentation @ http://docs.apphosted.com/index.html . Check them out, and make sure you let me know what you think.

*UPDATE*:

They are now open to the general public. 

Update:
-------
Read how this service stacks up against other services like it in my `Django hosting roundup <http://kencochrane.net/blog/2011/06/django-hosting-roundup-who-wins/>`_

2/16/2012: Full disclosure. On Feb 16th 2012, I accepted a job with dotCloud a competitor to apphosted. I plan on keeping this blog post up to date and impartial. If you think there are any errors, please let me know in the comments. 

