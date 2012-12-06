
:date: 2011-04-18 21:09:57
:tags: django,epio,deployment,hosting,python,paas
:category: blog
:slug: my-experiences-with-epio
:author: Ken Cochrane
:title: My Experiences with ep.io

Over the last decade I have deployed my applications many different ways, I have used, self managed dedicated servers, fully managed dedicated servers, Virtual Privates Servers from Linode, RackSpace and Amazon, shared hosting from webfaction, and I also used Google App Engine. I have learned a lot of things along the way, but the one thing I learned the most is that managing the server and keeping it up and running isn't fun. The fun part is writing the applications, and watching them grow as people start to use them. If there was only a way to write the application and then let someone else manage all of the server stuff for you, for a reasonable price. 

The Ruby on Rails folks have had services like this for a while, both Heroku and EngineYard are pretty popular and make hosting your Rails applications much easier. When Heroku was bought by salesforce.com for $212M, it opened people eyes, and started to get them thinking. Why can't we do that for Django? I have been wanting to build a Django service like this for a while now, but with limited time and not knowing where to begin, my idea went no where. Recently there have been a bunch of  new services that have popped up that provided turn key Django hosting, very similar in nature to Heroku, and Google App Engine (Python, and Java). This has gotten me very excited, and I plan on trying them all out.

One of these new services is called `ep.io <http://ep.io>`_, and it is run by Andrew Godwin (of Django South fame) and Ben Firshman. They are trying to make the hosting as simple as possible, so that you don't have to worry about servers at all. You write your application, deploy it to their service and they handle the rest. If you need to scale up your application, add load balancing, add more disk space, they will take care of that. This allows you the developer to spend your valuable time writing code instead of doing server maintenance. Best of all their pricing is based on usage, and they have a free tier, so if you have an application that you put out there, but it isn't using any resources, or very few resources, it might not cost you anything at all. So there is nothing stopping you from trying it out.

`ep.io <http://ep.io>`_ is still in beta, and not available to the public yet. The only way to get access is to put your name on a waiting list, and wait until you are sent an invite. I was lucky enough to get an invite early on, and I have been playing around with `ep.io <http://ep.io>`_ for a new project that I'm working on.  I'm still in development with my application so it isn't public yet, but I have an app deployed and running. I personally feel that if you are lucky enough to be selected to a closed beta, that it is your duty to give as much feedback as possible, so that you can help make the application great. If you aren't going to be doing this, then you don't deserve the early access. That is why I'm writing this post, to help spread the word about ep.io, and to show people getting started with the service how easy it is to deploy their app.

Before you start using a service like `ep.io <http://ep.io>`_, you need to do your research to make sure you know what it is you are getting with the service. Services like this aim to make hard tasks easy, and sometimes in doing so, they need to sacrifice features and flexibility. Knowing the pros and cons about a service before hand will help set your expectations accordingly so that you aren't disappointed later on in the process. It is important to note that as of this writing, they are still in beta, and thus still a work in progress, so if you are reading this, make sure you look at their website for the most up to date information. I will try and come back and update this post as the service deploys new features, and my experience with the service grows.

**Application setup:**

Like most managed application services, you won't be able to deploy your application as is, you will need to make a few changes in order to get everything to work. Luckily for us, this step wasn't too hard. I used the documentation that ep.io provides along with the ep.io project skeleton (https://github.com/idangazit/epio_skel) as a good starting point. ep.io uses an ini based configuration file called epio.ini for all of your configuration information. The documentation does a pretty good job explaining the different sections, and if you look at the ep.io project skeleton, there is a good example of one already created for you.

ep.io controls all aspects of your environment and because of this you don't know what your database information is, but that is OK, because if you setup your django settings.py file correctly, they will handle all of that for you. Once again, checkout the skeleton project or the documentation for the recommended settings. 

**Dependencies:**

If your project is already using virtualenv and pip, this shouldn't be too difficult. If not, you will need to read up a little on pip and it's requirements files (http://pip.openplans.org/requirement-format.html) in order to make sure you load all of your dependencies correctly. ep.io already has some of the most common libraries installed, for a full list, follow this link: http://www.ep.io/docs/runtime/#python-libraries. If you need a non pure-python library that isn't on their list, just let them know and if it is reasonable, they will most likely install it for you. 


**Deployment:**

ep.io offers a simple control panel so that you can see what apps you have installed, how much they are costing you, how many resources they are using (database, bandwidth, CPU, disk usage, etc). It also allows you to configure your domains, set application permissions, and view the console log. Besides that, you need to do everything using their command line client. Before you can use the client, you will need to install it, you can do that using either pip or easy install.

.. code-block:: bash

    pip install -U epio
    
    # or
    
    easy_install -U epio

Once you have the client installed, this is where the fun begins. With the client you can create, suspend, resume, upload or delete your app. You can also use the client to kick off remote commands on your server such as django syncdb. See the official documentation for full details: http://www.ep.io/docs/client/

Here are some notes and examples.

.. code-block:: bash

    #create app
    epio create [<app_name>]
    
    # suspend app
    epio suspend [-a <app_name>]
    
    #resume app
    epio resume [-a <app_name>]
    
    # delete app
    epio delete [-a <app_name>]
    
    # django syncdb 
    epio django [-a <app_name>] syncdb
    
    # django run south migrations for all apps
    epio django [-a <app_name>] migrate
    
    # django run south migrations for just one app called chicken
    epio django [-a <app_name>] migrate chicken
    
    # bash command
    epio run_command [-a <app_name>] bash
    
    # psql access to your database.
    epio run_command [-a <app_name>] psql


**Uploading App:**

The epio upload command will use git in the background to sync up your local directory to your server. It will ignore the .pyc files and such, if you have other files and directories that you also want to ignore you can create a file called .epioignore and list the files and directories to ignore in it. The .epioignore file has the same syntax as a .gitignore file.

The upload command is fine for most cases, but if you are already using git or mercurial, you can push your changes directly to ep.io, this allows you to do more of a continuous deployment setup, where you want to push to a central repo, run a bunch of tests and if it works push out to production. See this link for more info on uploading via git and mercurial http://www.ep.io/docs/vcss/


**Database:**

The ep.io databases are behind a firewall for security purposes, and because of this, you don't have direct access to the database, so if you are used to using a GUI database client, you are out of luck. The only way to get to your database right now is using the psql command tool. 

.. code-block:: bash

    # psql access to your database.
    epio run_command [-a <app_name>] psql


**Getting data into your databases:**

There are two recommended ways for getting data into your database.

You can create a SQL dump file, and add it to your project, and upload. Once it is up on the server you can run the following command.
  
.. code-block:: bash 
 
    epio run_command -- psql -f dumpname.sql

You can also stream the dump over the network via SSH. (They suggest that you only do this with dumps that are 20MB or less in size.)

.. code-block:: bash

    epio run_command psql < dumpname.sql


**Background tasks:**

ep.io supports both cronjobs and background tasks via Celery and Redis.

Cron is pretty easy to setup, you have a section in the epio.ini file called cron where you put your normal cron commands. The syntax isn't exactly the same, so see the documentation for the differences. http://www.ep.io/docs/epioini/#cron-section 

You can use either plain celery or django-celery, what ever you want, they support most features, but they currently don't support periodic tasks, they hope to get to that in the future. In the meantime just use a cron for those.


ep.io vs traditional hosting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I originally wrote this Pro's and Con's section at stackoverflow.com, and I include it here as well.
http://stackoverflow.com/questions/5117395/django-hosting-on-ep-io/5648323#5648323 

**Pros:**
---------

- *Server Management*: You don't have to worry about your server setup at all, it handles everything for you. With a VPS, you would need to worry about making sure the server is up to date with security patches, and all that fun stuff, with this, you don't worry about anything, they take care of all that for you.
-  *Deployment*: It makes deploying an app and having it up and running really quickly. deploying a new version of an app is a piece of cake, I just need to run one maybe two commands, and it handles everything for me.
- *Pricing*: you are only charged for what you use, so if you have a very low traffic website, it might not cost you anything at all.
- *Scaling*: They handle scaling and load balancing for you out of the box, no need for you to worry about that. You still need to write your application so that it can scale efficiently, but if you do, they will handle the rest.
- *Background tasks*: They have support for cronjobs as well as background workers using celery.
- *Customer support*: I had a few questions, sent them an email, and had an answer really fast, they have been great, so much better then I would have expected. If you run your own VPS, you really don't have anyone to talk to, so this is a major plus.

**Cons:**
---------

- *DB access*: You don't have direct access to the database, you can get to the psql shell, but you can't connect an external client GUI. This makes doing somethings a little more difficult or slow. But you can still use the django admin or fixtures to do a lot of things.
- *Limited services available*: It currently only supports Postgresql and redis, so if you want to use MySQL, memcached, mongodb,etc you are out of luck.
- *Low level c libs*: You can't install any dependencies that you want, similar to google app engine, they have some of the common c libs installed already, and if you want something different that isn't already installed you will need to contact them to get it added. http://www.ep.io/docs/runtime/#python-libraries
- *Email*: You can't send or receive email, which means you will need to depend on a 3rd party for that, which is probably good practice anyway, but it just means more money.
- *File system*: You have a more limited file system available to you, and because of the distributed nature of the system you will need to be very careful when working from files. You can't (unless i missed it) connect to your account via (s)ftp to upload files, you will need to connect via the ep.io command line tool and either do an rsync or a push of a repo to get files up there.


Update:
-------
Read how this service stacks up against other services like it in my `Django hosting roundup <http://kencochrane.net/blog/2011/06/django-hosting-roundup-who-wins/>`_

2/16/2012: Full disclosure. On Feb 16th 2012, I accepted a job with dotCloud a competitor to ep.io. I plan on keeping this blog post up to date and impartial. If you think there are any errors, please let me know in the comments. 


