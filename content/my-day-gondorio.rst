:date: 2011-04-22 06:12:41
:tags: gondor,django,python,hosting,paas
:category: blog
:slug: my-day-gondorio
:author: Ken Cochrane
:title: My Day in Gondor.io

The other day I wrote about a new `Django hosting service called ep.io <http://kencochrane.net/blog/2011/04/my-experiences-with-epio/>`_
, after I made that post, I was lucky enough to get an invite for the private beta of `gondor.io <http://gondor.io>`_, which is similar to `ep.io <http://ep.io>`_ but from the folks over at `Eldarion <http://eldarion.com/>`_. In order to test out the service I decided to take my Dango blog application and deploy it to Gondor and I kept notes along the way, here are those notes.

The sign up process was pretty typical, register and then validate your email address. Once into the system you are offered the ability to create a site. So I created my site "KenCochrane_blog" and it gave me a key which I'll use later on. Not knowing where to start I headed over to the `documentation <https://gondor.io/support/>`_. Which, as of this writing, is pretty basic, which is understandable since they are still in beta. I'm assuming the documentation will get better as they move forward. The current documentation and this blog post should get you enough information to get going.

Setting up my development environment:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Gondor uses a file to store your login credentials, so that you don't need to type it in everytime. It is pretty basic, here is how I installed mine on my MacBook Pro (OSX 10.6).

.. code-block:: bash

     # create the file, and edit it.
     $ emacs ~/.gondor

     # copy this into the file.

     [auth]
     username = <my_username>
     password = <my_password>

     # change the permissions so that only you can access it.
     $ chmod 600 ~/.gondor


Like all cool projects these days, gondor uses pip and virtualenv, I'm assuming you already have virtualenv and pip installed so I'll move onto the fun stuff.

.. code-block:: bash

     # make my virtualenv called gondor
     $ mkvirtualenv gondor

From this point on, all of these commands are done in the new gondor virtual environment that I just created. Gondor uses a command line client to manage your application, we need to install that before we can do anything.

.. code-block:: bash

          $ pip install gondor

Since I'm going to need to make changes to my blog, I decided to fork it and make all of my changes to gondor on the new fork. The new fork is on bitbucket and it is called kencochranenet_gondor. Now that I have it forked I can pull it down locally.

.. code-block:: bash

     # go to my projects directory and clone my blog.
     $ cd ~/projects
     $ hg clone https://bitbucket.org/kencochrane/kencochranenet_gondor kencochranenet_gondor
     $ cd kencochranenet_gondor/mysite

Now that we have some code to deploy, lets introduce the code to gondor. We use the init command inside of our django project and it will create a .gondor directory with a config file and some defaults.

.. code-block:: bash

     $ gondor init <site_key>

Gondor expects your project to be in a certain layout in order to work. For more info see the documentation: https://gondor.io/support/project-layout/

Since my blog didn't have everything in the right place, I need to add some directories and move some files around. One of the files I needed to add was deploy/wsgi.py, here is what it contains. Notice the two sys.path.insert lines. I added those because the `gondor documentation <https://gondor.io/support/setting-up-django/>`_ told me too.

.. code-block:: python

    import os, sys
    
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir, os.pardir)))
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)))
    
    from django.core.handlers.wsgi import WSGIHandler
    os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"
    application = WSGIHandler()
         

I also had to add the same sys.path lines to my manage.py settings. Here is my new manage.py

.. code-block:: python
  
    #!/usr/bin/env python
    from django.core.management import execute_manager
    import sys
    import os
    
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir, os.pardir)))
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)))
    
    try:
        import settings # Assumed to be in the same directory.
    except ImportError:
        sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
        sys.exit(1)
    
    if __name__ == "__main__":
        execute_manager(settings)

Gondor will automagically add your database and other settings to your app for you at deployment, and in order for that to work correctly you need to add the following at the end of your settings.py file.

.. code-block:: python
    
    try:
        from local_settings import *
    except ImportError:
        pass
    
    

My blog is using south to manage south migrations, so we need to edit the .gondor/config file to enable this.

.. code-block:: bash

    # edit .gondor/config changed migrations to migrations=south
    emacs .gondor/config
    
    # change this line
    migrations = None
    # to
    migrations = south

Now that we have made all of the changes that we need. I need to commit all of my changes. It is important to note that because gondor uses mecurial or git for managing your project files, you need to always remember to add new files and commit all changes before you try to deploy your application. 

***********
Deployment:
***********

Next step is deployment. Before we get there, we need to create a new instance. Gondor allows you to deploy multiple versions of your code, this lets you have a production version and development versions all running at the same time. Gondor calls these different deployments 'instances'. We run the 'gondor create master' command, which will create a new instance called, you guessed it, 'master', and this is what you should see.

.. code-block:: bash

    $ gondor create master
    Reading configuration... [ok]
    Creating instance on Gondor... [ok]   
    
    Run: gondor deploy master HEAD
    Visit: http://jg437.o1.gondor.io/

This created the master instance and tells us what our url for the instance will be. Now according to the log message I just need to run 'gondor deploy master HEAD' and that will deploy my app. Lets do that now.

.. code-block:: bash

    $ gondor deploy master HEAD
      Reading configuration... [ok]
      ERROR: could not map 'HEAD' to a SHA

As you can see, it didn't work, after lots of digging, I realized that the code was assuming I was on a branch called HEAD, which wasn't correct. I think HEAD is the default git branch, and in mercirual, it is default. Just to be sure, I checked my mercurial branch.

.. code-block:: bash

    $ hg summary
    
    parent: 122:76f0c2271b7f tip
     gondor settings
    branch: default
    commit: (clean)
    
    update: (current)

Running the quick 'hg summary' command lets me know that my branch is default, so I then made the changes to my command and reran the script.

.. code-block:: bash

    $ gondor deploy master default
    
    Reading configuration... [ok]
    Building tarball from default... [ok]
    Pushing tarball to Gondor... 
    Deploying... [failed]
    
    pip has failed installing your requirements. Here is the output we saw:
    
    Downloading/unpacking Django==1.2.5 (from -r mysite/requirements/project.txt (line 1))
    Creating supposed download cache at /var/gondor/instances/.cache-i194/pip-download
      Storing download in cache at ./.cache-i194/pip-download/http%3A%2F%2Fpypi.python.org%2Fpackages%2Fsource%2FD%2FDjango%2FDjango-1.2.5.tar.gz
      Running setup.py egg_info for package Django
    
    Downloading/unpacking MySQL-python==1.2.3c1 (from -r mysite/requirements/project.txt (line 2))
      Storing download in cache at ./.cache-i194/pip-download/http%3A%2F%2Fpypi.python.org%2Fpackages%2Fsource%2FM%2FMySQL-python%2FMySQL-python-1.2.3c1.tar.gz
      Running setup.py egg_info for package MySQL-python
        sh: mysql_config: not found
        Traceback (most recent call last):
          File "<string>", line 14, in <module>
          File "/var/gondor/instances/.cache-i194/pip-build/MySQL-python/setup.py", line 15, in <module>
            metadata, options = get_config()
          File "setup_posix.py", line 43, in get_config
            libs = mysql_config("libs_r")
          File "setup_posix.py", line 24, in mysql_config
            raise EnvironmentError("%s not found" % (mysql_config.path,))
        EnvironmentError: mysql_config not found
        Complete output from command python setup.py egg_info:
        sh: mysql_config: not found
    
    Traceback (most recent call last):
    
      File "<string>", line 14, in <module>
    
      File "/var/gondor/instances/.cache-i194/pip-build/MySQL-python/setup.py", line 15, in <module>
    
        metadata, options = get_config()
    
      File "setup_posix.py", line 43, in get_config
    
        libs = mysql_config("libs_r")
    
      File "setup_posix.py", line 24, in mysql_config
    
        raise EnvironmentError("%s not found" % (mysql_config.path,))
    
    EnvironmentError: mysql_config not found
    
    
    Command python setup.py egg_info failed with error code 1


We had mysql-python in our requirements file, and gondor doesn't support mysql, so we need to remove that, commit and try again.

.. code-block:: bash

    $ gondor deploy master default
    
    Reading configuration... [ok]
    Building tarball from default... [ok]
    Pushing tarball to Gondor... 
    Deploying... [failed]

    unable to build static (collectstatic or build_static not found)


closer but no cigar, gondor uses staticfiles (new in django 1.3 or django-staticfiles) to manage static files. If you aren't currently using static files add django-staticfiles to your pre django 1.3 app, or upgrade to django 1.3 and configure static files. To be honest, this was the biggest problem I had, it took me a while to get this correct. I was lucky enough to get some help on the #gondor IRC channel, which helped me along the way. With all of my changes made I committed them and tried again.

.. code-block:: bash

    $ gondor deploy master default
    Reading configuration... [ok]
    Building tarball from default... [ok]
    Pushing tarball to Gondor... 
    Deploying... [ok]

That worked!! woo hoo! now if I go to the URL (http://jg437.o1.gondor.io/) I got earlier, I should see something if all went well. I went to the site, and bingo, all working.. no data but it is there. Now how do I create my django admin user? Normally that is done when you do your initial syncdb, and since that is done by gondor, it doesn't give you a chance. Looking thru all of the documentation I didn't find anything. So I went and looked at the gondor client source code, and I found my answer. I kicked off the following command, answered the prompts and bingo, I was in business.

.. code-block:: bash

    $ gondor run master createsuperuser


**********
Conclusion
**********

Now that I have my app up and running and I have admin access I could switch over my blog to the new service if I wanted. I'll hold off for right now, but you get the picture. All and all I think this is going to be a nice service once they are fully up and running. It isn't as far along as ep.io, but I'm sure it won't be long before they are caught up. I'll try and keep this post updated as I learn more about the service and they release new features.


Update:
-------
Read how this service stacks up against other services like it in my `Django hosting roundup <http://kencochrane.net/blog/2011/06/django-hosting-roundup-who-wins/>`_

2/16/2012: Full disclosure. On Feb 16th 2012, I accepted a job with dotCloud a competitor to gondor.io. I plan on keeping this blog post up to date and impartial. If you think there are any errors, please let me know in the comments. 

