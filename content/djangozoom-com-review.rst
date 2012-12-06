
:date: 2011-06-05 11:17:11
:tags: django,python,deployment,hosting,djangozoom,paas
:category: blog
:slug: djangozoom-com-review
:author: Ken Cochrane
:title: DjangoZoom.com Review

This is part five in my series on django hosting services. Previously, I looked at `ep.io <http://kencochrane.net/blog/2011/04/my-experiences-with-epio/>`_, `apphosted.com <http://kencochrane.net/blog/2011/05/apphosted-com-django-hosting-review/>`_, `gondor.io <http://kencochrane.net/blog/2011/04/my-day-gondorio/>`_, `dotcloud.com <http://kencochrane.net/blog/2011/04/deploying-my-django-application-to-dotcloud/>`_ and now I'm looking at `DjangoZoom.com <http://DjangoZoom.com>`_. 

DjangoZoom.com is the brain child of Nate Aune and Shimon Rura and is based in Boston, Massachusetts. It was founded in 2010 at `StartupWeekend Boston <http://startupweekend.org/>`_ and was a finalist in the `MassChallenge <http://www.masschallenge.org/>`_. Their office is in the `Dogpatch Labs <http://dogpatchlabs.com/>`_ space for startups in Cambridge, Massachusetts. They are currently still in a closed beta, but they were nice enough to send me an invite to check it out. 

Normally when I check out a service for the first time, I look over the documentation to see what it can do, and what it can't do, and what I need to do in order to get my app up and running. DjangoZoom has a nice collection of documents that help guide you through the process of getting your application up and running on their platform. You need to be logged in, in order to read the documents, so I won't be able to link to any documents here, but if you are lucky enough to get an invite to DjangoZoom, I would check out the documents first, they will make the process much easier. They answer most of the common questions that you will have, and if you can't find your answer you can send them a message and they are very fast to respond.

After reading the documents I learned a few things. First off, DjangoZoom is a little different then the other services, all of the previous services that I have reviewed ep.io, dotcloud, apphosted, gondor.io, had a command line client that you use to push your application up onto their servers. 

DjangoZoom doesn't have a command line client at all, they only have a web based control panel that you use to install and configure your application. Also, instead of pushing your application code up on to their servers, they pull the code down from your code repository at build time. Most of the other services try and make it so that you can run any python/wsgi based application, where as DjangoZoom, is only supporting Django applications.

Not having a command line client has it's pros and cons. The main advantage of not having a command line client is simplicity. No need to install anything on your machine in order to deploy your code, all you need is a web browser. You can deploy your code from anywhere you have an internet connection. Making the application deployment as easy as possible will open up their service to people that are less technical, and might not be comfortable installing a command line client and running commands. The disadvantages of using just a web based console is that you are limited to what you can do in a browser. This is going to be less and less of an issue going forward as web browsers are getting more and more powerful all of the time. Also, just because they only offer a web based console now, doesn't mean they can't add a command line client later. 

Just like all of the other reviews I'm going to test out the system by deploying my blog onto their system and see how it goes.  My blog is currently hosted on bitbucket.org which uses mercurial, and currently djangozoom.com only offers support for git. In order to use djangozoom.com I needed to make a fork of my blog and put it on github. You can find my fork here: https://github.com/kencochrane/kencochrane_blog . They recommend github for git hosting, but you can use just about any git repo that is publicly accessible. If you have a private git repo, and you are on github just add the user djangozoom as a collaborator on your project. If you aren't on github and you have a private repo, you can add their public key to your repo, and it will give them permission to access your git repository from their servers. 

Install Process
---------------------

Once I had my code up on github I needed to make a few changes in order for it to work correctly, nothing major just needed to make my settings.py file a little more standard, which was pretty typical for the other services as well. Now that I had that done, I was ready to login to DjangoZoom and setup my application. Registering and logging into DjangoZoom was pretty straight forward, it was the same process as most online services, so just about anyone could do it with their eyes closed. 

After I logged in, I was able to add my application, here are the steps that I took to get my application up and running.

    Clicked on "add a new project"
    
    Put in repo url: git://github.com/kencochrane/kencochrane_blog.git  
    
    (Only SSH authentication is supported, so use either an unauthenticated public URL, or an SSH url (e.g. git@github.com:yourname/project.git.   On github.org, use the Git Read-Only URL if your repo is public, or the SSH URL if private.)
    
    Hit Next.
    
    Entered my title "kencochrane_blog"
    
    selected django 1.3
    
    settings module : mysite.settings
    
    static media location : "static /site-media"
    
    no additional directories to add to python path
    
    put in my requirements.txt file, so that it knows where to find my pip requirements. You don't need to do this, djangozoom will scan your projects and find this out for you, but it didn't work for me, I have an issue with my application that I wasn't able to find, and it was causing issues with their autoscanner. I think this is more my fault then theirs. 
    
    not putting in any extra requirements.
    
    base(repo) python package: put mysite.settings because my settings.py and root urls.py are at the top level of your repository. normally I don't do this, but I was following the example of this repo https://github.com/natea/mezzanine-site
    
    Checked the "ready to roll, deploy my project now" check box and hit next

At first I had some errors with my requirements, I needed to remove django and mysql and update the python-twitter lib. Once I did that, it worked like a charm. The whole deploy process only took 2 minutes and 45 seconds. 

Wow that was fast, pretty impressive considering it needed to pull down all of the code from github, and download a ton of dependencies, and then do what ever it needs to do to set it up on to their servers. After talking with them about this, they said they hope to get it even faster, which would be pretty impressive.
 
Now that I have my app deployed I can change some of the settings. 

    I created an alias to for my app to http://kencochrane.djangozoom.net
    
    You can also add a hostname like kencochrane.net.

    you can add a wildcard hostname as well. \*.kencochrane.net. 
    
    You can create a django superuser.  
    
    You can also run any of your manage.py commands right from the web console.

This whole process was pretty straight forward and didn't take long to complete. Now that I have done it with one application, it will be much easier for the next one.

Cool Feature Request
-------------------------------
Currently DjangoZoom makes it really easy to deploy your application to their servers. What would be cool is if they would make it easy to deploy common django applications to their service. For example on their blog they have a video to show how easy it is to `deploy django-cms to DjangoZoom <http://djangozoom.com/blog/2011/03/15/deploying-django-cms-45-seconds-djangozoom/>`_. 

In the video it shows them going out to github, forking and copying the link to the project, and then making some minor changes on the djangozoom settings page to get it to work correctly, and then it deploys. These steps weren't complicated but you needed to know what to do in order to get it to work. What if they made this a one step process? 

Click on a "install django-cms" link, and then their service would do what it needs to do to get it up and running on their service, and then returns you to a page where you can configure the app, add a django admin user, change the url, etc. That would allow someone who doesn't know anything about django an easy way to get a django-cms based website in no time. They could add one click installs for all kinds of common django projects, and expand outside of the developer community, which would expand their customer base. Those customers are the ones that really don't want to worry about server deploys and server management, and they are the ones that will pay more for those features. 

I'm sure this feature isn't on their roadmap, but I just thought I would throw it out there and see what people have to say about it. 

DjangoZoom.com status
----------------------------

DjangoZoom is still in closed beta, which means they are not done with it yet, and there may be some occasional bugs that pop up here and there, but that is expected. Another thing about a beta is that not all of the features are finished yet. So before you jump in and try and get your application up and running, check and make sure that your application can run correctly on the service with the features they have available so far. Here is a run down of all the different features your application might need and where they stand in DjangoZoom today.

Logging
^^^^^^^
You currently can't view your django or nginx logs at this time, they are working on this feature and hope to have it so that you can view your logs in the web based console in the future. In the meantime you can use a tool like django-sentry to view your django-logs.

SSL
^^^
Not available yet.

Caching
^^^^^^^
They currently don't support a caching server, they want to make sure they set it up correctly so that it is reliable and so that it is secure. In the meantime you can use django local memory caching.

Database
^^^^^^^^
They support PostgreSQL 8.4, if you are using mysql you will need to convert your app to support PostgreSQL. Since the Django ORM handles this by default, this shouldn't be a big deal unless you did something custom. No direct database access available. Loading data into system only supported by using django dumpdata/loaddata

Background tasks
^^^^^^^^^^^^^^^^
Not available yet, celery support possible in the future.

Cronjobs
^^^^^^^^
Not supported, they recommend `Advanced Python Scheduler <http://packages.python.org/APScheduler/>`_ or  `django-cron <https://github.com/reavis/django-cron>`_ which should run on their system.

Shell Access
^^^^^^^^^^^^
Not supported

API
^^^
Not available yet, one planned for the future.

Command line client
^^^^^^^^^^^^^^^^^^^
Not available yet, one planned for the future. Use the web base control panel.

Version control
^^^^^^^^^^^^^^^
Currently only supports git.

Videos
^^^^^^
Here are some videos of the DjangoZoom.com deployment process.

.. raw:: html 
 
    <p><iframe title="YouTube video player" width="480" height="390" src="http://www.youtube.com/embed/NCQxqw94Cgs" frameborder="0"></iframe></p>

.. raw:: html 

    <p><iframe title="YouTube video player" src="http://www.youtube.com/embed/DSe6R1ByS5k" width="480" frameborder="0" height="390"></iframe></p>


Conclusion
^^^^^^^^^^
I really enjoyed playing with DjangoZoom, it is quick and easy to use, it is still missing some key features that some people will need, but I'm sure they will add those soon enough. I wish them luck, and I can't wait to see them go live to the general public.


Update:
-------
Read how this service stacks up against other services like it in my `Django hosting roundup <http://kencochrane.net/blog/2011/06/django-hosting-roundup-who-wins/>`_

2/16/2012: Full disclosure. On Feb 16th 2012, I accepted a job with dotCloud a competitor to DjangoZoom. I plan on keeping this blog post up to date and impartial. If you think there are any errors, please let me know in the comments. 

